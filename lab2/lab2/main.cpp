#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <sstream>

#include "ValidInput.h"
#include "GeneralFunctions.h"
#include "UserInterface.h"

using namespace std;

enum main_menu {
	MANUAL_FILL_CHOICE = 1,
	RANDOM_FILL_CHOICE = 2,
	FROM_FILE_FILL_CHOICE = 3
};

int main() {
	setlocale(LC_ALL, "ru");
	vector<int> vec;
	vector<int> result_vec;
	srand(time(0));

	cout << "Лабораторная работа №2" << endl
		<< "Выполнил: Белоуско Георгий Константинович, гр: 444" << endl
		<< "Разработка программных систем" << endl
		<< "Вариант 12: Сортировка выбором / Selection sort" << endl;

	int main_menu_choice = 0;
	while (0 >= main_menu_choice || main_menu_choice > 3) {
		vec.clear();
		cout << "Выберите способ ввода данных: " << endl
			<< "1.Ввод данных с консоли" << endl
			<< "2.Ввод случайных данных" << endl
			<< "3.Ввод данных из файла" << endl;
		main_menu_choice = get_positive_int();

		switch (main_menu_choice)
		{
		case MANUAL_FILL_CHOICE:
			manual_fill_vec(vec);
			break;
		case RANDOM_FILL_CHOICE:
			random_fill_vec(vec);
			break;
		case FROM_FILE_FILL_CHOICE:
			from_file_fill_vec(vec);
			if (vec.size() == 0) {
				main_menu_choice = 0;
				cout << "Файл содержит недопустимые или невалидные данные" << endl;
			}
			break;
		default:
			cout << "Такого варианта выбора не сущесвтует" << endl;
			main_menu_choice = 0;
			break;
		}
		if (vec.size() != 0) {
			cout << "Исходный массив:" << endl;
			show_vec(vec);
			result_vec = selection_sort(vec);
			cout << "Отсортированный массив:" << endl;
			show_vec(result_vec);

			save_to_file(vec, result_vec);
		}
		else {
			continue;
		}
	}



	return 0;
}