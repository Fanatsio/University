using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class FlashingLight : MonoBehaviour
{
    public float constantIntens;
	public float inten;
	private float TimeDown;

	// Use this for initialization
	void Start () {
		TimeDown = 1.0f;
	}
	
	// Update is called once per frame
	void Update () {
		
		if(gameObject.GetComponent<Light>().intensity != constantIntens) gameObject.GetComponent<Light>().intensity = constantIntens;
		
		if(TimeDown > 0) TimeDown -= Time.deltaTime;
		
		if(TimeDown < 0) TimeDown = 0;
		
		if(TimeDown == 0) {
			inten = Random.Range(0.2f, 4.0f);
			gameObject.GetComponent<Light>().intensity = inten;
			TimeDown = Random.Range(0.2f, 0.6f);
		}
	}
}
