#include <iostream>
#include <string>

using namespace std;


class A {


    
public:
    string big = "nwdqidqwljwwwdqwqbbufniqwwfof;eonfifnwwjoejiwf;fqf;'d,qpwokdqodqwjopqiinjcmomopjorinnirbniob;nrino;iobregjirgjrjgejigrjgierogjriejoigrjjiergjioejeigorjiergijejogriejiojiejgirjigorjigojiregjioegrijge";
    
    void wtf(int a, int b, int c, int d, int e, int f, int g, int h, int i, int j, int k, int l, int m, int n, int o, int p, int q, int r) {
        std::cout << big.substr(a, b) << std::endl;
                std::cout << big.substr(c, d) << std::endl;
        std::cout << big.substr(e, f) << std::endl;
        std::cout << big.substr(g, h) << std::endl;
                std::cout << big.substr(i, j) << std::endl;
        std::cout << big.substr(k, l) << std::endl;
        std::cout << big.substr(m, n) << std::endl;
        std::cout << big.substr(a, b) << std::endl;
        std::cout << big.substr(c, d) << std::endl;
        std::cout << big.substr(e, f) << std::endl;
            std::cout << big.substr(g, h) << std::endl;
    }


    int count() {
        int count = 0;
        for (long unsigned int i = 0; i < big.size(); i++) {
            if (big[i] == ';') {
                count++;
            }
        }
        return count;
    }

};

int main() {
    A a;


    cout << a.count() << endl;
    return 0;
}