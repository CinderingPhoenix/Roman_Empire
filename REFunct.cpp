#include "REProj.h"

using namespace std;

// Float player stat. functs.
float playerAVG(vector<int> a) {
    int AB = a[1]; // At Bats
    int H = a[3];  // Hits
    float avg = 0.0f;

    if (AB > 0) {
        avg = static_cast<float>(H) / static_cast<float>(AB);
    }
    else {
        return 0;
    }
    return round(avg * 1000.0f) / 1000.0f; // Return rounded AVG
}

float playerOBP(vector<int> a) {
    int AB = a[1]; // At Bats
    int H = a[3];  // Hits
    int BB = a[9]; // Walks
    int IBB = a[10]; // Intentional Walks
    int HBP = 0; // Hit By Pitch (not included in the original vector)
    int SF = 0; // Sacrifice Flies (not included in the original vector)
    
    float obp = 0.0f;

    if (AB + BB + IBB + HBP > 0) {
        obp = static_cast<float>(H + BB + IBB + HBP) / static_cast<float>(AB + BB + IBB + HBP);
    }
    else {
        return 0;
    }
    return round(obp * 1000.0f) / 1000.0f; // Return rounded OBP
}

float playerSLG(vector<int> a) {
    int H = a[3]; // Total Bases
    int AB = a[1]; // At Bats
    int TwB = a[5]; // Doubles
    int ThB = a[6]; // Triples
    int HR = a[7]; // Home Runs
    int XBH = TwB + ThB + HR; // Extra Base Hits (Doubles + Triples + Home Runs)
    int OB = H - XBH; // Other Bases (not included in the original vector)
    float SLG = 0.0f;

    if (AB > 0) {
        int TBB = OB + (TwB * 2) + (ThB * 3) + (HR * 4); // Total Bases Batted
        SLG = static_cast<float>(TBB) / static_cast<float>(AB);
    }
    else {
        return 0;
    }
    return round(SLG * 1000.0f) / 1000.0f; // Return rounded SLG
}

float playerOPS(vector<int> a) {
    float obp = playerOBP(a);
    float slg = playerSLG(a);
    float ops = obp + slg;

    return round(ops * 1000.0f) / 1000.0f; // Return rounded OPS
}

float playerBABIP(vector<int> a, vector<int> b) {
    // BABIP = (H - HR) / (AB - SO - HR + SF)

    int AB = a[1]; // At Bats
    int H = a[3];  // Hits
    int HR = a[7]; // Home Runs
    int SO = a[11]; // Strikeouts
    int SF = b[4]; // Sacrifice Flies

    if (AB - SO - HR + SF > 0) {
        float babip = static_cast<float>(H - HR) / static_cast<float>(AB - SO - HR + SF);
        return round(babip * 1000.0f) / 1000.0f; // Return rounded BABIP
    }
    else {
        return 0;
    }
}