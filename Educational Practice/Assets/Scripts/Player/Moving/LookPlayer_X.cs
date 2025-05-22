using System.Collections;
using System.Collections.Generic;
using UnityEngine;
//СКРИПТ ДЛЯ ПОВОРОТА МОДЕЛИ ВО ВРЕМЯ ПОВОРОТА КАМЕРЫ
public class LookPlayer_X : MonoBehaviour
{
    public float sensHor;

    // Update is called once per frame
    void Update()
    {
        transform.Rotate(0, Input.GetAxis("Mouse X") * sensHor, 0);
    }
}
