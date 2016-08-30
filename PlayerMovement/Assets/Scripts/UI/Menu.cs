using UnityEngine;
using System.Collections;
using UnityEngine.SceneManagement;

public class Menu : MonoBehaviour {

	public void GoToLevel(string levelName) {
		SceneManager.LoadScene (levelName);
	}
}
