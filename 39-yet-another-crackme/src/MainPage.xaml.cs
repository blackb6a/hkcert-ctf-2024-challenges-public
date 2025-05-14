using System.Collections.Generic;
using System.Text;
namespace CrackMe
{
    public partial class MainPage : ContentPage
    {
        public MainPage()
        {
            InitializeComponent();
        }

        async private void OnCounterClicked(object sender, EventArgs e)
        {
            if (checkFlag(FlagEntry.Text))
            {
                await DisplayAlert("Correct", "Congrat, that is the correct flag!", "OK");
            }
            else
            {
                await DisplayAlert("Wrong", "Not the right flag", "OK");
            }
        }
        private bool checkFlag(string f)
        {
            int[] m1 = { 9, 10, 11, 12, 13, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126 };
            int[] m2 = { 58, 38, 66, 88, 78, 39, 80, 125, 64, 106, 48, 49, 98, 32, 42, 59, 126, 93, 33, 56, 112, 120, 60, 117, 111, 45, 87, 35, 10, 68, 61, 77, 11, 55, 121, 74, 107, 104, 65, 63, 46, 110, 34, 41, 102, 97, 81, 12, 47, 51, 103, 89, 115, 75, 54, 92, 90, 76, 113, 122, 114, 52, 72, 70, 50, 94, 91, 73, 84, 95, 36, 82, 124, 53, 108, 101, 9, 13, 44, 96, 67, 85, 116, 123, 100, 37, 43, 119, 71, 105, 118, 69, 99, 79, 86, 109, 62, 83, 40, 57 };
            ulong[] s = { 16684662107559623091UL, 13659980421084405632UL, 11938144112493055466UL, 17764897102866017993UL, 11375978084890832581UL, 14699674141193569951UL };
            ulong KEY = 0xCAFEBABECAFEBABE;
            int BLOCKSIZE = 8;
            Dictionary<int, int> M = new Dictionary<int, int>();
            for (int i = 0; i < m1.Length; i++)
            {
                M[m1[i]] = m2[i];
            }

            StringBuilder s1 = new StringBuilder();
            foreach (char c in f)
            {
                s1.Append((char)M[(int)c]);
            }

            int padSize = BLOCKSIZE - (f.Length % BLOCKSIZE);
            string a = s1.ToString() + new string('\x01', padSize);
            List<ulong> s2 = new List<ulong>();
            for (int i = 0; i < a.Length - 1; i += BLOCKSIZE)
            {
                byte[] blockBytes = Encoding.ASCII.GetBytes(a.Substring(i, BLOCKSIZE));
                ulong block = BitConverter.ToUInt64(blockBytes, 0);
                s2.Add(block);
            }

            List<ulong> s3 = new List<ulong>();
            foreach (ulong block in s2)
            {
                ulong t = KEY ^ block;
                s3.Add(t);
            }

            for (int i = 0; i < s.Length; i++)
            {
                if (s[i] != s3[i])
                {
                    return false;
                }
            }
            return true;
        }
    }

}
