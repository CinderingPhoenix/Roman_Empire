#include "testproj.h"

using namespace std;

int main() {

    vector<string> wdarfs = {"Wilyer", "David", "Abreu", "RF", "L", "L"};
    vector<int> wdarfnCS = {81, 265, 39, 68, 133, 11, 0, 18, 52, 28, 4, 68, 5, 2};
    vector<int> wdarfnACS = {295, 29, 0, 0, 2, 6, 38, 1123, 0, 131, 1};

    vector<float> wdarfnf = {playerAVG(wdarfnCS), 
                             playerOBP(wdarfnCS), 
                             playerSLG(wdarfnCS), 
                             playerOPS(wdarfnCS), 
                             0.0f, // Placeholder for GO/AO
                             playerBABIP(wdarfnCS, wdarfnACS)};

    cout << "Name: " << wdarfs[0] << " " << wdarfs[1] << " " << wdarfs[2] << endl;
    cout << "Position: " << wdarfs[3] << endl;
    cout << "Bats: " << wdarfs[4] << endl;
    cout << "Throws: " << wdarfs[5] << endl << endl;
    cout << "Player 2025 Stats:" << endl;
    cout << "Games: " << wdarfnCS[0] << "\t| At Bats: " << wdarfnCS[1] << "\t| Runs: " << wdarfnCS[2] << "\t| Hits: " << wdarfnCS[3] << endl;
    cout << "Total Bases: " << wdarfnCS[4] << "\t| Doubles: " << wdarfnCS[5] << "\t| Triples: " << wdarfnCS[6] << "\t| Home Runs: " << wdarfnCS[7] << endl;
    cout << "Runs Batted In: " << wdarfnCS[8] << "\t| Walks: " << wdarfnCS[9] << "\t| Intentional Walks: " << wdarfnCS[10] << "\t| Strike Outs: " << wdarfnCS[11] << endl;
    cout << "Stolen Bases: " << wdarfnCS[12] << "\t| Caught Stealing: " << wdarfnCS[13] << endl << endl;
    cout << "Player 2025 Advanced Stats:" << endl;
    cout << "Plate Appearances: " << wdarfnACS[0] << "\t| Extra Base Hits: " << wdarfnACS[1] << "\t| Hit by Pitch: " << wdarfnACS[2] << "\t| Sacrifice Bunts: " << wdarfnf[3] << endl;

    return 0;

    // CS:
     //     G,    AB,     R,     H,    TB,    2B,    3B,    HR,   RBI,    BB,    IBB,     SO,     SB,     CS,  AVG,  OBP,  SLG,  OPS, GO/AO
     // CS[0], CS[1], CS[2], CS[3], CS[4], CS[5], CS[6], CS[7], CS[8], CS[9], CS[10], CS[11], CS[12], CS[13], F[0], F[1], F[2], F[3], F[4]
    // ACS:
     // PA, XBH, HBP, SAC, SF, BABIP, GIDP, GIDPO, NP, P/PA, ROE, LOB, WO
     // ACS[0], ACS[1], ACS[2], ACS[3], ACS[4], ACS[5], F[6], ACS[7], ACS[8], ACS[9], ACS[10], ACS[11], ACS[12]
}