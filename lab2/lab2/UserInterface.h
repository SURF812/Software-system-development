#pragma once
enum save_menu {
	SAVE_YES_CHOICE = 1,
	SAVE_NO_CHOICE = 2
};

void show_vec(std::vector<int> vec);
void save_to_file(std::vector<int>vec, std::vector<int> result_vec);
bool is_read_only_file(std::string path);