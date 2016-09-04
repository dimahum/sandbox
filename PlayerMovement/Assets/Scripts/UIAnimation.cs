using UnityEngine;
using System.Collections;

public class UIAnimation : MonoBehaviour {

	public float animationTime = 3.0f;

	private	bool animationStarted = false;
	private float startTimeStamp = 0.0f;

	// Use this for initialization
	void Start () {
		var renderer = GetComponent<SpriteRenderer> ();
		renderer.enabled = false;
	}
	
	// Update is called once per frame
	void Update () {
		if (animationStarted) 
		{
			var renderer = GetComponent<SpriteRenderer> ();
			if (!renderer.enabled)
				renderer.enabled = true;
			else if (Time.time - startTimeStamp > animationTime)
			{
				renderer.enabled = false;
				animationStarted = false;
			}
				
		}
	}

	public void StartAnimation()
	{
		animationStarted = true;
		startTimeStamp = Time.time;
	}
}
