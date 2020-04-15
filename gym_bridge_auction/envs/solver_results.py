from gym_bridge_auction.envs.game import *

# wartości punktowe z zapisu brydżowego plus dodatkowe punkty wykorzystywane do wyznaczenia optymalnego kontraktu
# i funkcji nagrody
POINTS = {'C': 20, 'D': 20, 'H': 30, 'S': 30, 'NT': (40, 30), 'FAIL': -50, 'BONUS': 50}


def get_results_from_solver(pbn):
    """Funkcja wyznaczająca liczbę lew jaką weźmie każdy z graczy dla danego miana.
    Wykorzystano Double Dummy Solver napisany w C++"""

    # biblioteka umożliwiająca połączenie C++ i Python
    import cppyy

    cppyy.include("./solver/dds_wrapper/ddswrapper.h")
    cppyy.load_library("ddswrapper")

    solver_results = cppyy.gbl.calcHands(cppyy.gbl.std.string(pbn))

    return list(solver_results)


def get_solver_result_for_player(player_index, solver_result):
    """Funkcja zwracająca rezultat z solvera dla danego gracza"""

    player_solver_result = {}

    for i in range(0, len(BIND_SUIT) - 1):
        player_solver_result[BIND_SUIT[3 - i]] = solver_result[5 * player_index + i]

    player_solver_result[BIND_SUIT[len(BIND_SUIT) - 1]] = solver_result[5 * player_index + (len(BIND_SUIT) - 1)]

    return player_solver_result


def max_contract_for_suit(player_solver_result):
    """Funkcja zwracająca maksymalny kontrakt dla danego miana"""

    player_max_contract = {}

    for i in range(0, len(BIND_SUIT)):
        player_max_contract[BIND_SUIT[i]] = player_solver_result[BIND_SUIT[i]] - 6

        if player_max_contract[BIND_SUIT[i]] < 0:
            player_max_contract[BIND_SUIT[i]] = 0

    return player_max_contract


def calc_point_for_contract(player_max_contract):
    """Funkcja wyliczająca ilość punktów jaką można zdobyć za ugrany dany kontrakt"""

    point_for_contracts = {}
    point_for_contracts['C'] = POINTS['C'] * player_max_contract['C']
    point_for_contracts['D'] = POINTS['D'] * player_max_contract['D']
    point_for_contracts['H'] = POINTS['H'] * player_max_contract['H']
    point_for_contracts['S'] = POINTS['S'] * player_max_contract['S']

    if player_max_contract['NT'] == 0:
        point_for_contracts['NT'] = 0
    else:
        point_for_contracts['NT'] = POINTS['NT'][0] + (player_max_contract['NT'] - 1) * POINTS['NT'][1]

    return point_for_contracts


def choose_best_contracts(point_for_contracts):
    """Funkcja wybierająca najbardziej punktowane miano kontraktu dla danego gracza"""

    best_contracts_colours = []
    values_list = list(point_for_contracts.values())
    keys_list = list(point_for_contracts.keys())
    max_value = max(values_list)

    for element in enumerate(values_list):
        if element[1] == max_value:
            best_contracts_colours.append(keys_list[element[0]])

    return best_contracts_colours

