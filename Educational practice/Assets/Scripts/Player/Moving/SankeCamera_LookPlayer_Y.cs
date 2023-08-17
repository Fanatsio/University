using System.Collections;
using System.Collections.Generic;
using UnityEngine;

//ТРЯСКА КАМЕРЫ И ПОВОРОТ ГОЛОВЫ ПО Y
public class SankeCamera_LookPlayer_Y : MonoBehaviour
{
    public float amount = 1;
    public float speed = 1;
    public float sensVert = 9;

    //Поворот камеры, чтобы шею не свернуть
    public float minVert = -45;
    public float maxVert = 45;

    float rotationX = 0;

    Vector3 startPos;
    float distation;
    Vector3 rotation = Vector3.zero;

    // Start is called before the first frame update
    void Start()
    {
        startPos = transform.position;    
    }

    // Update is called once per frame
    void Update()
    {
        //Ось y
        rotationX -= Input.GetAxis("Mouse Y") * sensVert;
        rotationX = Mathf.Clamp(rotationX, minVert, maxVert);

        //Ось z
        distation += (transform.position - startPos).magnitude;
        startPos = transform.position;
        rotation.z = Mathf.Sin(distation * speed) * amount;
        transform.localEulerAngles = new Vector3(rotationX, transform.localEulerAngles.y, rotation.z);
    }
}
