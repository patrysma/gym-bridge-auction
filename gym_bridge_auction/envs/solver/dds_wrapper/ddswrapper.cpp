
#include "ddswrapper.h"

std::vector <int> calcResults(ddTableResults * table)
{
    //Zwraca rezultaty najpierw dla North w kolejności: S, H, D, C, NT
    //Potem gracza dla East, South i West
    std::vector <int> result;

    for (int j = 0; j < DDS_HANDS; j++)
    {
        for (int i = 0; i < DDS_STRAINS; i++)
        {
            result.push_back(table->resTable[i][j]);
        }
    }

    return result;
}

std::vector <int> calcNumberOfTricks(std::string pbnHands)
{
    ddTableDealPBN tableDealPBN;
    ddTableResults table;
    int res;
    char line[80];

#if defined(__linux) || defined(__APPLE__) //ilość wątków
  SetMaxThreads(0);
#endif

    char pbn[80];
    strcpy(pbn, pbnHands.c_str()); //zamiana rąk w stringach na char

    strcpy(tableDealPBN.cards, pbn); //wczytanie rąk do odpowiedniej zmiennej wykorzystywanej w funkcji poniżej

    res = CalcDDtablePBN(tableDealPBN, &table); //wyliczenie ilości lew jaką wezmą gracze z partnerem dla danego miana

    if (res != RETURN_NO_FAULT) //sprawdzenie błędów
    {
        ErrorMessage(res, line);
        printf("DDS error: %s\n", line);
    }

    std::vector <int> result = calcResults(&table);

    return result; //wektor wyników dla poszczególnych graczy
}

int calcOptimumContracts(std::string pbnHands, int dealer)
{
    int res;
    char line[80];
    ddTableResults table;
    parResultsDealer pres;
    ddTableDealPBN tableDealPBN;

#if defined(__linux) || defined(__APPLE__) //ilość wątków
  SetMaxThreads(0);
#endif

    char pbn[80];
    strcpy(pbn, pbnHands.c_str()); //zamiana rąk w stringach na char

    strcpy(tableDealPBN.cards, pbn); //wczytanie rąk do odpowiedniej zmiennej wykorzystywanej w funkcji poniżej

    res = CalcDDtablePBN(tableDealPBN, &table); //wyliczenie ilości lew jaką wezmą gracze z partnerem dla danego miana

    if (res != RETURN_NO_FAULT) //sprawdzenie błędów
    {
        ErrorMessage(res, line);
        printf("DDS error: %s\n", line);
    }

    res = DealerPar(&table, &pres, dealer, 0); //wyznaczenie optymalnego kontraktu dla danego rozdania

    if (res != RETURN_NO_FAULT)
    {
        ErrorMessage(res, line);
        printf("DDS error: %s\n", line);
    }

    return pres.score; //liczba punktów dla pary N-S za optymalny kontrakt
}







