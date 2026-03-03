#include <vector>
#include <string>
#include "CppUnitTest.h"
#include "../lab2/GeneralFunctions.h"
#include "../lab2/ValidInput.h"
#include "../lab2/UserInterface.h"

using namespace Microsoft::VisualStudio::CppUnitTestFramework;

namespace Lab2_tests
{
	TEST_CLASS(Lab2_tests)
	{
	public:

		TEST_METHOD(selection_sort_Test)
		{
			std::vector<int> input_vec = { 6,5,6,7,3,1,8,12,65,-12 };
			std::vector<int> result_vec = selection_sort(input_vec);
			std::vector<int> control_vec = { -12,1,3,5,6,6,7,8,12,65 };

			for (int i = 0; i < result_vec.size(); i++)
			{
				Assert::AreEqual(result_vec[i], control_vec[i]);
			}

			input_vec = { 65,12,-23,344,6577,2 };
			result_vec = selection_sort(input_vec);
			control_vec = { -23,2,12,65,344,6577 };

			for (int i = 0; i < result_vec.size(); i++)
			{
				Assert::AreEqual(result_vec[i], control_vec[i]);
			}
		}

		TEST_METHOD(is_num_Test)
		{
			std::string str1 = "12";
			std::string str2 = "-56";
			std::string str3 = "asd";
			std::string str4 = "34q23";

			Assert::IsTrue(is_num(str1));
			Assert::IsTrue(is_num(str2));
			Assert::IsFalse(is_num(str3));
			Assert::IsFalse(is_num(str4));
		}

		TEST_METHOD(is_read_only_file_Test)
		{
			std::string url1 = "../../lab2/forTests/readOnly.txt";
			std::string url2 = "../../lab2/notReadOnly.txt";

			Assert::IsTrue(is_read_only_file(url1));
			Assert::IsFalse(is_read_only_file(url2));
		}
	};
}
