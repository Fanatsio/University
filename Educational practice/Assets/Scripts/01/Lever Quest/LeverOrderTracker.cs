using System.Collections;
using System.Collections.Generic;
using UnityEngine;
/*
    private int[] correctOrder = {1, 2, 3}; // Правильный порядок нажатия рычагов
*/
public class LeverOrderTracker : MonoBehaviour
{
    public AudioSource audioSource; // Ссылка на компонент AudioSource
    public AudioClip correctCombinationSound; // Аудиоклип для воспроизведения при правильной комбинации
    public AudioClip wrongCombinationSound; // Аудиоклип для воспроизведения при неправильной комбинации


    private int[] correctOrder = {1, 2, 3}; // Правильный порядок нажатия рычагов
    private int currentIndex = 0; // Текущий индекс в порядке нажатия
    private bool combinationSolved = false; // Флаг, указывающий, что комбинация рычагов решена

    public void SetCorrectOrder(int[] order)
    {
        correctOrder = order;
    }

    public void CheckLeverOrder(int leverNumber)
    {
        if (combinationSolved)
        {
            return; // Если комбинация рычагов уже решена, прекратить дальнейшую проверку
        }

        if (correctOrder == null)
        {
            Debug.LogError("Правильный порядок рычагов не задан!");
            return;
        }

        if (leverNumber == correctOrder[currentIndex])
        {
            currentIndex++;

            if (currentIndex >= correctOrder.Length)
            {
                // Рычаги были нажаты в правильном порядке
                Debug.Log("Порядок рычагов верный!");
                combinationSolved = true; // Установить флаг, что комбинация рычагов решена
                PlayCorrectCombinationSound(); // Воспроизвести звук при правильной комбинации
                // Здесь можно выполнить дополнительные действия, когда порядок рычагов верный
            }
        }
        else
        {
            // Рычаги были нажаты в неправильном порядке
            Debug.Log("Порядок рычагов неверный!");
            PlayWrongCombinationSound(); // Воспроизвести звук при неправильной комбинации
            // Здесь можно выполнить дополнительные действия, когда порядок рычагов неверный
            // Например, сбросить текущий прогресс или показать сообщение об ошибке
            ResetLeverOrder();
        }
    }

    private void ResetLeverOrder()
    {
        currentIndex = 0;
        combinationSolved = false; // Сбросить флаг, что комбинация рычагов решена
        // Здесь можно добавить дополнительные действия для сброса состояния порядка рычагов
    }

    private void PlayCorrectCombinationSound()
    {
        if (audioSource != null && correctCombinationSound != null)
        {
            audioSource.PlayOneShot(correctCombinationSound); // Воспроизведение звулкаудиоклипа при правильной комбинации
        }
    }

    private void PlayWrongCombinationSound()
    {
        if (audioSource != null && wrongCombinationSound != null)
        {
            audioSource.PlayOneShot(wrongCombinationSound); // Воспроизведение звулкаудиоклипа при неправильной комбинации
        }
    }
}