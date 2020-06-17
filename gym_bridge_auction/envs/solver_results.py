from gym_bridge_auction.envs.game import *
# biblioteka umożliwiająca połączenie C++ i Python
import cppyy

# wartości punktowe z zapisu brydżowego do wyznaczenia funkcji nagrody
CONTRACT_POINTS = {'C': 20, 'D': 20, 'H': 30, 'S': 30, 'NT': (40, 30), 'X': 2, 'XX': 4}
PENALTY_POINTS = {'NO DOUBLE/REDOUBLE': 50, 'DOUBLE': (100, 2), 'REDOUBLE': (200, 2)}
BONUS = {'SLAM': 500, 'GRAND_SLAM': 1000, 'PARTIAL-GAME': 50, 'GAME': 300, 'DOUBLE': 50, 'REDOUBLE': 100,
         'OVERTRICKS_DOUBLE': 100, 'OVERTRICKS_REDOUBLE': 200}


def get_results_from_solver(pbn, dealer):
    """Funkcja wyznaczająca liczbę lew, jaką weźmie każdy z graczy wraz z partnerem dla danego miana 
    oraz zwracająca wartość punktową dla pary N-S (dla E-W jest taka sama wartość, tylko z przeciwnym znakiem) 
    za optymalny kontrakt, gdy wszystkie pary licytują idealnie.
    Wykorzystano Double Dummy Solver napisany w C++.
    Wyznaczone liczby lew są w następującej kolejności:
    najpierw North i ilość lew dla poszczególnych mian kolejno: S, H, D, C, NT,
    a następnie East, South i West z identyczną kolejnością mian."""

    try:
        cppyy.include("./gym_bridge_auction/envs/solver/dds_wrapper/ddswrapper.h")
        cppyy.load_library("ddswrapper")
        solver_result = cppyy.gbl.calcNumberOfTricks(cppyy.gbl.std.string(pbn))
        optimum_score = cppyy.gbl.calcOptimumContracts(cppyy.gbl.std.string(pbn), dealer)

        return list(solver_result), optimum_score
    except:
        print('Solver error')
        quit()


def get_solver_result_for_player(player_index, solver_result):
    """Ilość lew dla danego miana z solvera jaką weźmie ustalony gracz"""

    player_solver_result = {}

    for i in range(0, len(BIND_SUIT) - 1):
        player_solver_result[BIND_SUIT[3 - i]] = solver_result[5 * player_index + i]

    player_solver_result[BIND_SUIT[len(BIND_SUIT) - 1]] = solver_result[5 * player_index + (len(BIND_SUIT) - 1)]

    return player_solver_result


def max_contract_for_suit(player_solver_result):
    """Maksymalny kontrakt dla danego miana - liczba"""

    player_max_contract = {}

    for i in range(0, len(BIND_SUIT)):
        player_max_contract[BIND_SUIT[i]] = player_solver_result[BIND_SUIT[i]] - 6

        if player_max_contract[BIND_SUIT[i]] < 0:
            player_max_contract[BIND_SUIT[i]] = 0

    return player_max_contract
