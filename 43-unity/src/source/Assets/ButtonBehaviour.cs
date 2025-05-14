using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class GameBehaviour : MonoBehaviour
{
    int stage = 0;
    string current_flag = "hkcert24{";
    string charList = "0123456789abcdefghijklmnopqrstuvwxyz";
    public Text TxtMessage;
    public Text TxtChallenge;
    public InputField InputName;

    public GameObject scrollViewItem;

    public Transform scrollView;

    int[] name_length = {1, 2, 3, 4, 5, 6};
  
    // Flag: hkcert24{1_4m_on3_5t4r_und3r_c4e1um}
    string[] target_result = {
      "ESFP ISTP ESFJ ISFJ ESTJ ISTP ESTP ENFP ENTJ ESTJ ISTP ISTJ ISFJ ENFJ ESFP ISFP ESTP ISFP INTP ENFP ISTJ ESFJ ENTP ISTJ ISFJ ISFJ ESFP ESFJ ENFP INTP INTP ISFJ ENFJ ISTP INFP ENFP ISTJ ISFJ ESFJ ISTP INFP ESFJ ENFP ESFP ESFP ISTP ESFJ ISTJ ENFP ISTJ",
      "ISFJ ESTP ESTJ INTJ ISTP ISFJ ESFJ ISFJ ISTJ INTP ENFP ISTP ENFJ ISTJ INFP ISFP ISFP INTJ ISFJ ESFJ ISFJ ESTJ ESFP INTP ESFJ ESFJ ISFP ISFJ ESFP INTP ISFP ENFJ ISFP ESFP ESFJ ISFJ ESFP ESFP ESTP ESTP ISTP INTP ESFJ ESFJ ENFP ESFP ISFJ ISTJ ISFP ISTP",
      "ISTJ ESFJ ISFJ INTJ ESFJ ISFP ISFJ ESFJ ESFP ISFP ESTJ ISFP ENFP ENTJ INFP ESTP ISFJ INFP ISTJ ISFP INFP ESFJ ISTJ ISTJ ISFP ISFP ESFP ESTJ ESTJ INTP ESFP ISFJ ESFJ ESFJ ISFJ ISFJ ESTJ ESFP ESTJ ISTJ ENFP ESFJ ESFP ENFJ ESFJ ESFP ESFJ ESFJ ESFP ISFP",
      "INFP ESFJ ISFJ ENFP ESFJ ISFP INFP ENTJ ESFP ESTP ESFP ESFP INFP ESTP ISTJ ESFJ ISTP INTP ISFP ESTJ ISFJ ENFP ESTP ENFJ ISFJ ISTP ESFJ ESFJ ESFJ ESFJ ESFJ ESTJ INTP ISFJ ISFP ESFP ENFJ INTP ESTP ISFJ ESFP ISFJ ISTJ ISTJ ISTP ENFP ENFP ISFP ISFJ INTP",
      "ESFJ ISFP ESFJ ISFJ ISTJ ENFJ ESTJ ESTJ ISFP ISFP ESFJ ENTP ENFP ISTJ ISTP INTJ ISTJ ISFJ ESFP ISTP ISFJ ENFJ ENFJ ISFJ INTP ESFJ ISTJ INTJ ISFJ ENTP ESFJ ESFJ ISTP ESTJ ENFP ISFJ ISFP ISFJ ESTJ ISFJ ENTP ENFP ESTJ ENFP ENFP ISFJ ESTP ISFJ ISFP INTP",
      "ESFJ ESFJ INFP ESFJ ESFP ISFJ ESTJ ESFJ ESTJ ISFJ ISFP ISFJ ISFJ INFP INFJ ENTP ESTJ ISTJ ISTP ISFJ INTJ ESTJ ISFP ISFP ESFP ISTJ ESTJ ESFJ INFP ESTP ISFJ ISFJ ESTJ ISTJ ENTJ ESFP ISTJ ESFJ ESFJ ISTJ INTJ ESTJ ENFP ESTP ISTP ISFP ISFJ ESFJ INTP ESTP"
    };
    // Start is called before the first frame update
    void Start()
    {
      stage = 0;
      UpdateChallenge();
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    int HashName(string name) {
      long result = 0;
      for (var i = 0; i < name.Length; ++i) {
        result *= 36;
        result += charList.IndexOf(name[i]);
        result &= 0xffffffff;
      }
      return (int)result;
    }

    bool ValidName(string name) {
      for (var i = 0; i < name.Length; ++i) {
        if (!charList.Contains(name[i])) {
          return false;
        }
      }
      return true;
    }

    void Roll(List<string> target, bool additem) {
        float value = UnityEngine.Random.value * 201;
        string selected;
        if (value < 54) { // N
          if (value < 33) { // NF
            if (value < 12) { // INF
              if (value < 3) {
                selected = "INFJ";
              } else {
                selected = "INFP";
              }
            } else if (value < 28) {
              selected = "ENFP";
            } else {
              selected = "ENFJ";
            }
          } else if (value < 44) { // INT
            if (value < 37) {
              selected = "INTJ";
            } else {
              selected = "INTP";
            }
          } else if (value < 50) {
              selected = "ENTP";
          } else {
              selected = "ENTJ";
          }
        } else if (value < 147) { // SxJ
          if (value < 105) { // ISxJ
            if (value < 77) {
              selected = "ISTJ";
            } else {
              selected = "ISFJ";
            }
          } else if (value < 122) {
            selected = "ESTJ";
          } else {
            selected = "ESFJ";
          }
        } else if (value < 176) { // ISxP
          if (value < 158) {
            selected = "ISTP";
          } else {
            selected = "ISFP";
          }
        } else if (value < 184) {
          selected = "ESTP";
        } else {
          selected = "ESFP";
        }
        target.Add(selected);
        if (additem) {
          GameObject item = Instantiate(scrollViewItem);
          item.GetComponentInChildren<Text>().text = selected;
          item.transform.SetParent(scrollView, false);
        }
    }

    void UpdateChallenge() {
      if (stage == name_length.Length) {
        TxtMessage.text = "Complete Flag: " + current_flag;
        TxtChallenge.text = "Congratulations! You have successfully found the flag!";
      } else {
        TxtMessage.text = "Partial Flag: " + current_flag;
        TxtChallenge.text = "Flag Challenge: Try to get \"" + target_result[stage].Substring(0, 12 * 5 - 1) + "\" with a " + name_length[stage].ToString() + "-character name.";
      }
    }


    public void OnClick() {
      string name = InputName.text;
      if (!ValidName(name.ToLower())) {
        TxtMessage.text = "Name can only be alphanumeric characters!";
        return;
      }
		  UnityEngine.Random.InitState(HashName(name.ToLower()));
      List<string> results = new List<string>();
      foreach (Transform child in scrollView.transform) {
        GameObject.Destroy(child.gameObject);
      }
      for (var i = 0; i < 50; ++i) {
        Roll(results, i < 12);
      }
      if (stage < name_length.Length && name.Length == name_length[stage] && string.Join(" ", results) == target_result[stage]) {
        current_flag += name.ToLower();
        stage += 1;
        if (stage == name_length.Length) {
          current_flag += "}";
        } else {
          current_flag += "_";
        }
      }
      UpdateChallenge();
    }
}
