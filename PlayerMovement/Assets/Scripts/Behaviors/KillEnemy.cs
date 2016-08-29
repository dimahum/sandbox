using UnityEngine;
using System.Collections;

public class KillEnemy : MonoBehaviour {

	// Use this for initialization
	void Start () {
	
	}
	
	// Update is called once per frame
	void Update () {
	
	}

	void OnCollisionEnter2D (Collision2D col)
	{
		if(col.gameObject.name.StartsWith("Enemy")) {
			//Die
			Destroy(col.gameObject);
		}
	}
}
