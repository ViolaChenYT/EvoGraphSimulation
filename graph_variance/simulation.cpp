#include <random>
#include <ctime>

#include <iostream>
#include <fstream>
#include <string>
#include <map>

#include <vector>
#include <stdexcept>
#include <set>
#include <cmath>
#include <numeric>

#include "Utilities.hpp"

using namespace std;

class Model {
private:
    int N;
    std::vector<double> s;
    std::vector<double> fitness_vector;

public:
    std::vector<int> gene_vector;

    Model(int, double, double);
    void BDProcess();
};

Model::Model(int N, double s1, double s2) {
    this->N = N;
    this->s.push_back(s1);
    this->s.push_back(s2);
    std::vector<int> zeros(N, 0);
    this->gene_vector = zeros;
    std::vector<double> ones(N, 1);
    this->fitness_vector = ones;

    this->gene_vector[0] = 1;
    int fit_type = binomial_sample(1, 0.5);
    this->fitness_vector[0] = 1 + s[fit_type];
}

void Model::BDProcess() {
    // Calculate Fitness
    double wild_type_fit = N - std::accumulate(gene_vector.begin(), gene_vector.end(), 0.0);
    double mutant_fit = std::inner_product(gene_vector.begin(), gene_vector.end(), fitness_vector.begin(), 0.0);

    // Birth
    int geno_type = binomial_sample(1, mutant_fit / (wild_type_fit + mutant_fit));
    int fit_type = binomial_sample(1, 0.5);

    // Death
    int death_pos = uniform_int_sample(0, N-1);

    // Update
    gene_vector[death_pos] = geno_type;
    fitness_vector[death_pos] = 1 + geno_type * s[fit_type];
}


int main() {
    ofstream file;
    string output_name = "result/simulation_100_var.txt";

    int iterations = 1e5;

    // Parameters
    int N = 100;
    // double s1 = -0.1;
    // double s2 = 0.1;
    double s1, s2, s_mean, s_var;

    std::vector<double> s_mean_list;
    s_mean_list.push_back(0);
    s_mean_list.push_back(0.05);
    s_mean_list.push_back(0.1);
    s_mean_list.push_back(0.2);

    std::vector<double> s_var_list;
    for (int i = 0; i <= 9; i++) {
        double s_temp = 0.1 * i;
        s_var_list.push_back(s_temp);
    }

    // std::vector<double> s1_list;
    // std::vector<double> s2_list;
    // for (int i = 0; i <= 20; i++) {
    //     double s_temp = double(i) / 10 - 1;
    //     s1_list.push_back(s_temp);
    //     s2_list.push_back(s_temp);
    // }

    // for (int i_s1 = 0; i_s1 < (s1_list.size() - 1); i_s1++) {
    //     for (int i_s2 = i_s1 + 1; i_s2 < s2_list.size(); i_s2++) {
    for (int i_s_mean = 0; i_s_mean < s_mean_list.size(); i_s_mean++) {
        for (int i_s_var = 0; i_s_var < s_var_list.size(); i_s_var++) {
            s_mean = s_mean_list[i_s_mean];
            s_var = s_var_list[i_s_var];
            s1 = s_mean - sqrt(s_var);
            s2 = s_mean + sqrt(s_var);
            // Run
            int fix_times = 0;
            double total_gen = 0;

            for (int i = 0; i < iterations; i++) {
                std::cout << i << std::endl;
                int generations = 0;
                Model trial(N, s1, s2);

                while (true) {
                    trial.BDProcess();
                    generations++;
                    int check_tag = std::accumulate(trial.gene_vector.begin(), trial.gene_vector.end(), 0.0);
                    if (check_tag == 0) {
                        break;
                    } else if (check_tag == N) {
                        total_gen += generations;
                        fix_times++;
                        break;
                    }
                }
            }

            double ave_gen = 0;
            if (fix_times != 0) {
                ave_gen = total_gen / fix_times;
            }
            file.open(output_name, ios::app);
            file << N << "\t";
            // file << s1 << "\t";
            // file << s2 << "\t";
            file << s_mean << "\t";
            file << s_var << "\t";
            file << iterations << "\t";
            file << fix_times << "\t";
            file << ave_gen << endl;
            file.close();
        }
    }
    std::cout << "Hello World!" << std::endl;
}
