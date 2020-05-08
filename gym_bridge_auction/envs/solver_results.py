from gym_bridge_auction.envs.game import *
#from gym_bridge_auction.envs.bridge_auction_env import cppyy
# biblioteka umożliwiająca połączenie C++ i Python
import cppyy

# wartości punktowe z zapisu brydżowego do wyznaczenia optymalnego kontraktu
# i funkcji nagrody
CONTRACT_POINTS = {'C': 20, 'D': 20, 'H': 30, 'S': 30, 'NT': (40, 30), 'X': 2, 'XX': 4}
PENALTY_POINTS = {'NO DOUBLE/REDOUBLE': 50, 'DOUBLE': (100, 2), 'REDOUBLE': (200, 2)}
BONUS = {'SLAM': 500, 'GRAND_SLAM': 1000, 'PARTIAL-GAME': 50, 'GAME': 300, 'DOUBLE': 50, 'REDOUBLE': 100}


def get_results_from_solver(pbn):
    """Funkcja wyznaczająca liczbę lew jaką weźmie każdy z graczy dla danego miana.
    Wykorzystano Double Dummy Solver napisany w C++
    Wyniki w następującej kolejności:
    najpierw North i ilość lew dla poszczególnych mian kolejno: S, H, D, C, NT
    następnie East, South i West"""

    cppyy.include("./solver/dds_wrapper/ddswrapper.h")
    cppyy.load_library("ddswrapper")

    solver_result = cppyy.gbl.calcNumberOfTricks(cppyy.gbl.std.string(pbn))

    return list(solver_result)


def get_optimum_contracts_from_solver(pbn, dealer):
    """Funkcja zwracająca wartość punktową dla pary N-S (dla E-W jest taka sama wartość, tylko z przeciwnym znakiem)
    za optymalny kontrakt wyznaczony za pomocą solvera, gdy wszystkie pary licytują idealnie"""

    optimum_score = cppyy.gbl.calcOptimumContracts(cppyy.gbl.std.string(pbn), dealer)

    return optimum_score


def get_solver_result_for_player(player_index, solver_result):
    """Funkcja zwracająca rezultat z solvera dla danego gracza"""

    player_solver_result = {}

    for i in range(0, len(BIND_SUIT) - 1):
        player_solver_result[BIND_SUIT[3 - i]] = solver_result[5 * player_index + i]

    player_solver_result[BIND_SUIT[len(BIND_SUIT) - 1]] = solver_result[5 * player_index + (len(BIND_SUIT) - 1)]

    return player_solver_result


def max_contract_for_suit(player_solver_result):
    """Funkcja zwracająca maksymalny kontrakt dla danego miana - liczbę"""

    player_max_contract = {}

    for i in range(0, len(BIND_SUIT)):
        player_max_contract[BIND_SUIT[i]] = player_solver_result[BIND_SUIT[i]] - 6

        if player_max_contract[BIND_SUIT[i]] < 0:
            player_max_contract[BIND_SUIT[i]] = 0

    return player_max_contract


# def calc_point_for_contract(player_max_contract):
#     """Funkcja wyliczająca ilość punktów jaką można zdobyć za ugrany dany kontrakt"""
#
#     point_for_contracts = {}
#
#     # punkty kontraktowe
#     for i in range(0, len(BIND_SUIT) - 1):
#         point_for_contracts[BIND_SUIT[i]] = CONTRACT_POINTS[BIND_SUIT[i]] * player_max_contract[BIND_SUIT[i]]
#
#     if player_max_contract['NT'] == 0:
#         point_for_contracts['NT'] = 0
#     else:
#         point_for_contracts['NT'] = CONTRACT_POINTS['NT'][0] + (player_max_contract['NT'] - 1) * CONTRACT_POINTS['NT'][
#             1]
#
#     # punkty za częściówki, dograne i szlemy i szlemiki
#     for i in range(0, len(BIND_SUIT)):
#         if point_for_contracts[BIND_SUIT[i]] != 0:
#             if point_for_contracts[BIND_SUIT[i]] < 100:
#                 point_for_contracts[BIND_SUIT[i]] += BONUS['PARTIAL-GAME']
#             else:
#                 point_for_contracts[BIND_SUIT[i]] += BONUS['GAME']
#
#             if player_max_contract[BIND_SUIT[i]] == 6:
#                 point_for_contracts[BIND_SUIT[i]] += BONUS['SLAM']
#             elif player_max_contract[BIND_SUIT[i]] == 7:
#                 point_for_contracts[BIND_SUIT[i]] += BONUS['GRAND_SLAM']
#
#     return point_for_contracts
#
#
# def choose_best_contracts(point_for_contracts):
#     """Funkcja wybierająca najbardziej punktowany kontrakt dla danego gracza"""
#
#     values_list = list(point_for_contracts.values())
#     max_value = max(values_list)
#
#     return max_value
