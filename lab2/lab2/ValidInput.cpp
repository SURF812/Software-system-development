#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include "ValidInput.h"

using namespace std;

int get_int() {
	int input = 0;
	cin >> input;
	if (cin.fail()) {
		cout << "Неверный тип данных. Введите корректное значение" << endl;
		while (cin.fail()) {
			cin.clear();
			cin.ignore(INT_MAX, '\n');
			cin >> input;
		}
	}
	cin.ignore(INT_MAX, '\n');
	return input;
}

int get_positive_int() {
	int temp = 0;
	while (temp <= 0) {
		temp = get_int();
		if (temp <= 0) {
			cout << "Число не может быть меньше или равно 0" << endl;
		}
	}
	return temp;
}

string get_valid_url() {
	string url = "";
	vector<char> SpecSymbol = { '<', '>', ':', '"', '|', '?', '*' };
	bool file_url_correct = true;

	while (url.empty()) {
		file_url_correct = true;
		cout << "Введите путь до файла" << endl;
		cin >> url;

		for (int i = 0; i < url.size(); i++)
		{
			if (file_url_correct)
			{
				if (url[i] == ':' && i == 1) { continue; }
				for (int j = 0; j < SpecSymbol.size(); j++)
				{
					if (url[i] == SpecSymbol[j]) {
						file_url_correct = false;
						url = "";
						cout << "Путь до файла не может содержать специальные символы" << endl;
					}
				}
			}
		}
	}
	return url;
}

bool is_num(string element)
{
	string felement = element;
	if (felement[0] == '-') {
		felement.erase(felement.begin());
	}
	for (int i = 0; i < felement.size(); i++)
	{
		if (!isdigit(felement[i])) {
			cout << "[!]Элемент " << element << " не является числом, проверьте корректность ввода" << endl;
			return false;
		}
	}
	return true;
}

void manual_fill_vec(vector<int>& vec) {
	int n = 0;
	string temp = "";
	vector<string> line_elements;
	cout << "Введите размер исходного массива:" << endl;
	n = get_positive_int();

	while (temp == "") {
		cout << "Введите " << n << " элементов через пробел" << endl;
		line_elements.clear();
		getline(cin, temp);
		istringstream iss(temp);
		while (iss >> temp) {
			line_elements.push_back(temp);
		}
		if (line_elements.size() > n) {
			cout << "В строке избыток элементов, введите данные еще раз" << endl;
			temp = "";
			continue;
		}
		if (line_elements.size() < n) {
			cout << "В строке недостаточно элементов, введите данные еще раз" << endl;
			temp = "";
			continue;
		}
		for (int i = 0; i < line_elements.size(); i++)
		{
			if (!is_num(line_elements[i])) {
				temp = "";
				vec.clear();
				break;
			}
			vec.push_back(stoi(line_elements[i]));
		}
	}
}

void random_fill_vec(vector<int>& vec) {
	int n = 0;
	cout << "Введите размер исходного массива" << endl;
	n = get_positive_int();

	for (int i = 0; i < n; i++)
	{
		vec.push_back(rand());
	}
}

void from_file_fill_vec(vector<int>& vec) {
	string url = "";
	url = get_valid_url();
	ifstream input(url);
	string line = "";
	string temp = "";

	if (input.is_open()) {
		input.seekg(0, ios::end);
		if (input.tellg() == 0) {
			cout << "Файл пуст" << endl;
			input.close();
			return;
		}
		input.seekg(0, ios::beg);

		getline(input, line);
		istringstream iss(line);
		while (iss >> temp) {
			if (!is_num(temp)) {
				vec.clear();
				return;
			}
			else {
				vec.push_back(stoi(temp));
			}
		}
	}

	input.close();
}

bool is_read_only_file(std::string path)
{
	ifstream file(path, std::ios::out | std::ios::app);

	if (!file.is_open()) {
		return true;
	}
	file.close();
	return false;
}