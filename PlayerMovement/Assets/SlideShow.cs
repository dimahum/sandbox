using UnityEngine;
using System.Collections;
using UnityEngine.SceneManagement;

public class SlideShow : MonoBehaviour
{

	public Sprite[] elements;

	private int currIndex = 0;

	public float minimum = 0.0f;
	public float maximum = 1.0f;
	public float duration = 5.0f;
	private float startTime;
	public bool fadeIn = false;

	public SpriteRenderer spriteRenderer;

	void Start ()
	{
		spriteRenderer = GetComponent<SpriteRenderer> ();
		spriteRenderer.sprite = elements [currIndex];
	}

	void Update ()
	{
		float t = (Time.time - startTime) / duration;
		if (t >= 1) {
			if (!fadeIn) {
				OnEndingAnimation ();
			} else {
				if (currIndex == elements.Length - 1)
					OnFinishSlideShow ();
				else
					LoadNextSlide ();
				
				OnStartingAnimation ();
			}
		}

		if (fadeIn)
			spriteRenderer.color = new Color (1f, 1f, 1f, Mathf.SmoothStep (maximum, minimum, t));
		else
			spriteRenderer.color = new Color (1f, 1f, 1f, Mathf.SmoothStep (minimum, maximum, t));        
	}

	void OnStartingAnimation ()
	{
		startTime = Time.time;
		fadeIn = false;
	}

	void OnEndingAnimation ()
	{
		startTime = Time.time;
		fadeIn = true;
	}

	void OnFinishSlideShow ()
	{
		SceneManager.LoadScene ("Level_0");
	}

	void LoadNextSlide ()
	{
		currIndex++;
		spriteRenderer.sprite = elements [currIndex];
	}
}
