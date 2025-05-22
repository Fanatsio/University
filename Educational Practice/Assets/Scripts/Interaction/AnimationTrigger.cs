using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class AnimationTrigger : MonoBehaviour
{
    public Animator animator; // Ссылка на компонент Animator
    public string animationTrigger = "TriggerAnimation"; // Имя параметра триггера анимации
    public float interactionDistance = 1f; // Максимальное расстояние для взаимодействия

    private void Update()
    {
        RaycastHit hit;
        Camera camera = GameObject.Find("Camera").GetComponent<Camera>();
        Ray ray = camera.ScreenPointToRay(Input.mousePosition);

        if (Physics.Raycast(ray, out hit, interactionDistance))
        {
            if (hit.collider.gameObject == gameObject && hit.distance <= interactionDistance)
            {
                PlayAnimation();
            }
        }
    }

    private void PlayAnimation()
    {
        if (animator != null)
        {
            animator.SetTrigger(animationTrigger);
        }
    }
}
