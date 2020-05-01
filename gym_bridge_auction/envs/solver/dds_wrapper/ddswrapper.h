#ifndef DDSWRAPPER_H
#define DDSWRAPPER_H

#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#include <string.h>
#include "../dds/include/dll.h"
#include <vector>

std::vector <int> calcResults(ddTableResults * table); //funkcja zapisująca wyliczenia lew do wektora

std::vector <int> calcNumberOfTricks(std::string pbnHands); //główna funkcja, obliczająca ile lew weźmie dany gracz z partnerem, gdy dane jest miano
//Jako parametr przyjmuje ręce graczy w formacie PBN
//Zwraca wektor wyników w kolejności:
//najpierw North i ilość lew dla poszczególnych mian kolejno: S, H, D, C, NT
//następnie East, South i West

int calcOptimumContracts(std::string pbnHands, int dealer);
//Funkcja zwracająca liczbę punktów dla pary N-S za optymalny kontrakt w danym rozdaniu
//Za parametr przyjmuje:
//Ręce graczy w formacie PBN
//Liczbę określającą, kto jest rozdającym

#endif // DDSWRAPPER_H
