using UnityEngine;
using System.Collections;

public class DeathAndRespawn : MonoBehaviour {

	private const string DEATH_TAG = "DeathTag";
	private const string RESPAWN_TAG = "RespawnTag";

	private float respawnX;
	private float respawnY;

	// Use this for initialization
	void Start () {
		Transform playerTransform = GetComponent<Transform> ();
		respawnX = playerTransform.position.x;
		respawnY = playerTransform.position.y;
	}
	
	// Update is called once per frame
	void Update () {
	
	}

	void OnTriggerEnter2D(Collider2D target){
		if (target.tag == RESPAWN_TAG) {
			respawnX = target.transform.position.x;
			respawnY = target.transform.position.y;
		} else if (target.tag == DEATH_TAG) {
			OnRespawn ();
		}

	}

	void OnRespawn() {
		transform.localPosition = new Vector3 (respawnX, respawnY);
	}
}
