using UnityEngine;
using System.Collections;

public class SimpleWalk : MonoBehaviour {

	public float speed = 40f;
	public float direction = 1.0f;
	protected Rigidbody2D body2d;

	protected virtual void Awake(){
		body2d = GetComponent<Rigidbody2D> ();
	}

	// Use this for initialization
	void Start () {
	
	}
	
	// Update is called once per frame
	void Update () {
		var velX = speed * direction;

		body2d.velocity = new Vector2(velX, body2d.velocity.y);
	}

	void OnCollisionEnter2D (Collision2D col)
	{
		if(col.gameObject.name.Contains("Wall") ||
			col.gameObject.name.StartsWith("Enem")) {
			direction *= -1.0f;
		}
	}
}
