using UnityEngine;
using System.Collections;
using UnityEngine.SceneManagement;
using UnityEngine.Events;

[System.Serializable]
public class SlideInfo
{
	public Sprite sprite;
	public string text;
}

public class SlideShow : MonoBehaviour
{

	public SlideInfo[] elements;
	public float duration = 5.0f;
	public UnityEvent unityEvent;

	private int currIndex = 0;
	private float minimum = 0.0f;
	private float maximum = 1.0f;
	private float startTime;
	private bool fadeIn = false;
	private SpriteRenderer spriteRenderer;
	private TextMesh subtitle;

	void Start ()
	{
		spriteRenderer = GetComponent<SpriteRenderer> ();
		subtitle = GetComponentInChildren<TextMesh> ();
		spriteRenderer.sprite = elements [currIndex].sprite;
		subtitle.text = elements [currIndex].text;
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
		if (unityEvent != null)
			unityEvent.Invoke ();
	}

	void LoadNextSlide ()
	{
		currIndex++;
		spriteRenderer.sprite = elements [currIndex].sprite;
		subtitle.text = elements [currIndex].text;
	}
}
