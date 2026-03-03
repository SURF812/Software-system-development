#include <iostream>
#include <vector>
#include <fstream>
#include "UserInterface.h"
#include "ValidInput.h"
#include "GeneralFunctions.h"

using namespace std;

void show_vec(vector<int> vec) {
	for (int i = 0; i < vec.size(); i++)
	{
		cout << vec[i] << " ";
	}
	cout << endl;
}

void save_to_file(vector<int>vec, vector<int> result_vec) {
	int save_menu_choice = 0;
	int rewrite_choice = 0;
	string url = "";

	cout << "Сохранить результат работы программы в файл?" << endl
		<< "1.Да" << endl
		<< "2.Нет" << endl;
	while (save_menu_choice == 0) {
		save_menu_choice = get_positive_int();
		if (save_menu_choice == SAVE_YES_CHOICE) {
			while (url == "") {
				rewrite_choice = 0;
				url = get_valid_url();
				if (url != "") {
					ifstream output(url);
					if (output.is_open()) {
						if (is_read_only_file(url)) {
							cout << "Файл находиться в режиме только для чтения" << endl;
							url = "";
							continue;
						}
						cout << "Файл уже существует, перезаписать?" << endl << "1.Да" << endl << "2.Нет" << endl;
						while (rewrite_choice != SAVE_YES_CHOICE && rewrite_choice != SAVE_NO_CHOICE) {
							rewrite_choice = get_int();
							if (rewrite_choice == SAVE_YES_CHOICE) {
								continue;
							}
							if (rewrite_choice == SAVE_NO_CHOICE) {
								url = "";
							}
							else {
								cout << "Такого варианта выбора не существует" << endl;
							}
						}
					}
				}
			}

			save_vector(vec, result_vec, url);
			cout << "Результат успешно сохранен" << endl;
		}
		else if (save_menu_choice == SAVE_NO_CHOICE) {
			return;
		}
		else {
			cout << "Такого варианта выбора не существует" << endl;
			save_menu_choice = 0;
		}
	}
}