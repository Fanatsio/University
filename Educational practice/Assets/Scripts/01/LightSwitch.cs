using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class LightSwitch : MonoBehaviour
{
    public float interactionDistance = 2f; // Максимальное расстояние для взаимодействия
    public float delayTime = 5f; // Задержка перед отключением света
    public AudioSource audioSource; // Ссылка на компонент AudioSource для проигрывания аудио
    public AudioClip audioClip; // Аудиоклип для проигрывания
    public Transform targetTransform; // Ссылка на Transform объекта, который нужно повернуть
    public Vector3 targetRotation; // Углы поворота, на которые нужно повернуть объект

    private bool lightsOn = true; // Изначально свет включен
    private bool interacted = false; // Флаг для отслеживания взаимодействия
    private float timer = 0f; // Таймер для отслеживания задержки

    private void Update()
    {
        if (!interacted && Input.GetMouseButtonDown(0))
        {
            RaycastHit hit;
            Camera camera = GameObject.Find("Camera").GetComponent<Camera>();
            Ray ray = camera.ScreenPointToRay(Input.mousePosition);

            if (Physics.Raycast(ray, out hit, interactionDistance))
            {
                if (hit.collider.CompareTag("Light"))
                {
                    interacted = true; // Установка флага взаимодействия
                    timer = delayTime; // Задаем значение таймера
                    ToggleLights(); // Выключаем свет
                    PlayAudio(); // Проигрываем аудио
                }
            }
        }

        if (interacted && timer > 0f)
        {
            timer -= Time.deltaTime; // Уменьшаем таймер
            if (timer <= 0f)
            {
                ToggleLights(); // Включаем свет после задержки
                StopAudio(); // Прекращаем проигрывание аудио

                if (targetTransform != null)
                {
                    targetTransform.rotation = Quaternion.Euler(targetRotation); // Поворачиваем объект
                }
            }
        }
    }

    private void ToggleLights()
    {
        lightsOn = !lightsOn;
        GameObject[] lights = GameObject.FindGameObjectsWithTag("Light");
        foreach (GameObject lightObj in lights)
        {
            Light lightComponent = lightObj.GetComponent<Light>();
            if (lightComponent != null)
            {
                lightComponent.enabled = lightsOn;
            }
        }
    }

    private void PlayAudio()
    {
        if (audioSource != null && audioClip != null)
        {
            audioSource.PlayOneShot(audioClip);
        }
    }

    private void StopAudio()
    {
        if (audioSource != null)
        {
            audioSource.Stop();
        }
    }
}





// using System.Collections;
// using System.Collections.Generic;
// using UnityEngine;

// /*
//             RaycastHit hit;
//             Camera camera = GameObject.Find("Camera").GetComponent<Camera>();
//             Ray ray = camera.ScreenPointToRay(Input.mousePosition);
// */

// public class LightSwitch : MonoBehaviour
// {
//     public float interactionDistance = 2f; // Максимальное расстояние для взаимодействия
//     public float delayTime = 5f; // Задержка перед отключением света
//     public AudioSource audioSource; // Ссылка на компонент AudioSource для проигрывания аудио
//     public AudioClip audioClip; // Аудиоклип для проигрывания
//     private bool lightsOn = true; // Изначально свет включен
//     private bool interacted = false; // Флаг для отслеживания взаимодействия
//     private float timer = 0f; // Таймер для отслеживания задержки

//     private void Update()
//     {
//         if (!interacted && Input.GetMouseButtonDown(0))
//         {
//             RaycastHit hit;
//             Camera camera = GameObject.Find("Camera").GetComponent<Camera>();
//             Ray ray = camera.ScreenPointToRay(Input.mousePosition);

//             if (Physics.Raycast(ray, out hit, interactionDistance))
//             {
//                 if (hit.collider.CompareTag("Light"))
//                 {
//                     interacted = true; // Установка флага взаимодействия
//                     timer = delayTime; // Задаем значение таймера
//                     ToggleLights(); // Выключаем свет
//                     PlayAudio(); // Проигрываем аудио
//                 }
//             }
//         }

//         if (interacted && timer > 0f)
//         {
//             timer -= Time.deltaTime; // Уменьшаем таймер
//             if (timer <= 0f)
//             {
//                 ToggleLights(); // Включаем свет после задержки
//                 StopAudio(); // Прекращаем проигрывание аудио
//             }
//         }
//     }

//     private void ToggleLights()
//     {
//         lightsOn = !lightsOn;
//         GameObject[] lights = GameObject.FindGameObjectsWithTag("Light");
//         foreach (GameObject lightObj in lights)
//         {
//             Light lightComponent = lightObj.GetComponent<Light>();
//             if (lightComponent != null)
//             {
//                 lightComponent.enabled = lightsOn;
//             }
//         }
//     }

//     private void PlayAudio()
//     {
//         if (audioSource != null && audioClip != null)
//         {
//             audioSource.PlayOneShot(audioClip);
//         }
//     }

//     private void StopAudio()
//     {
//         if (audioSource != null)
//         {
//             audioSource.Stop();
//         }
//     }
// }
