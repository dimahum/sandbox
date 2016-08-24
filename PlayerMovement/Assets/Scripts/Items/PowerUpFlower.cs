using UnityEngine;
using System.Collections;
using UnityEngine.SceneManagement;

public class PowerUpFlower : Collectable {

	public int itemID = 1;
	public GameObject projectilePrefab;

	override protected void OnCollect(GameObject target){

		if(SceneManager.GetActiveScene().name == "Level_1")
			SceneManager.LoadScene ("Level_0");
		else if(SceneManager.GetActiveScene().name == "Level_0")
			SceneManager.LoadScene ("Level_1");


		var equipBehavior = target.GetComponent<Equip> ();
		if(equipBehavior != null){
			equipBehavior.currentItem = itemID;
		}

		var shootBehavior = target.GetComponent<FireProjectile> ();
		if (shootBehavior != null) {
			shootBehavior.projectilePrefab = projectilePrefab;
		}
	}
}
