using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class LeverInteraction : MonoBehaviour
{
    public LeverOrderTracker orderTracker; // Ссылка на скрипт для отслеживания порядка нажатия
    public int leverNumber; // Номер этого рычага
    public float interactionDistance = 1.5f; // Дистанция взаимодействия с рычагом

    private void OnMouseDown()
    {
        if (orderTracker != null)
        {
            RaycastHit hit;
            Camera camera = GameObject.Find("Camera").GetComponent<Camera>();
            Ray ray = camera.ScreenPointToRay(Input.mousePosition);

            if (Physics.Raycast(ray, out hit, interactionDistance))
            // if (Physics.Raycast(ray, out hit, Mathf.Infinity))
            {
                if (hit.collider.gameObject == gameObject && hit.distance <= interactionDistance)
                {
                    orderTracker.CheckLeverOrder(leverNumber);
                }
            }
        }
    }
}