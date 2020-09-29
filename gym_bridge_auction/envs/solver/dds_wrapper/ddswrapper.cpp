
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

std::vector <int> calcTricksAndScore(std::string pbnHands, int dealer)
{
    int res1, res2;
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

    res1 = CalcDDtablePBN(tableDealPBN, &table); //wyliczenie ilości lew jaką wezmą gracze z partnerem dla danego miana

    if (res1 != RETURN_NO_FAULT) //sprawdzenie błędów
    {
        ErrorMessage(res1, line);
        printf("DDS error: %s\n", line);
    }

    std::vector <int> result = calcResults(&table); //wektor z liczbami lew dla wszystkich graczy

    res2 = DealerPar(&table, &pres, dealer, 0); //wyznaczenie optymalnego kontraktu dla danego rozdania

    if (res2 != RETURN_NO_FAULT) //sprawdzenie błędów
    {
        ErrorMessage(res2, line);
        printf("DDS error: %s\n", line);
    }

    result.push_back(pres.score); //dodanie liczby punktów dla pary N-S za optymalny kontrakt do wektora wyników

    return result; //wektor wyników
}







