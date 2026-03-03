#include <vector>
#include <fstream>
#include <string>
#include "GeneralFunctions.h"

using namespace std;

vector<int> selection_sort(const vector<int> input) {
    vector<int> result_vec = input;
    size_t n = result_vec.size();

    for (size_t i = 0; i < n - 1; i++) {
        size_t min_idx = i;

        for (size_t j = i + 1; j < n; j++) {
            if (result_vec[j] < result_vec[min_idx]) {
                min_idx = j;
            }
        }

        if (min_idx != i) {
            std::swap(result_vec[i], result_vec[min_idx]);
        }
    }

    return result_vec;
}

void save_vector(std::vector<int> vec, vector<int> result_vec, string url)
{
	ofstream output(url);
	output << "Исходный вектор:" << endl;
	for (int i = 0; i < vec.size(); i++)
	{
		output << vec[i] << " ";
	}
	output << endl << "Отсортированный вектор:" << endl;
	for (int i = 0; i < result_vec.size(); i++)
	{
		output << result_vec[i] << " ";
	}

	output.close();
}
