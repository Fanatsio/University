// ДЕЛАЛ ПО ЭТОМУ ГАЙДУ https://youtu.be/wOwJcMKiSfw?list=PL-7DNz4y0vum5XaDngv6aT9QxZupkt-DZ
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PlayerSoundsWalk : MonoBehaviour
{
    //МАССИВ ЗВУКОВ
    public AudioClip[] map_1_walk, map_2_walk, map_1_run, map_2_run;
    private AudioSource source;
    private AudioClip clip;
    [SerializeField]
    private float timer = 0.5f;
    private bool stop;


    private void Start() {
        source = GetComponent<AudioSource>();
    }

    public void PlayStep(string nameMap) {
        if (!GetComponent<MovePlayer>().Run_Player)
        {
            timer = 0.5f;
            switch (nameMap) {
                //ВАЖНО ЧТОБЫ ПОВЕРХНОСТЬ В ЮНИТИ НАЗЫВАЛАСЬ ТАКЖЕ КАК В CASE
                case "Map_1":
                    clip = map_1_walk[Random.Range(0, map_1_walk.Length)];
                    break;

                case "Map_2":
                    clip = map_2_walk[Random.Range(0, map_2_walk.Length)];
                    break;
            }
        }
        //ЗВУКОВ ДЛЯ БЕГА НЕТ XDDDDDDDD
        else {
            timer = 0.3f;
            switch (nameMap) {
                case "Map_1":
                    clip = map_1_run[Random.Range(0, map_1_run.Length)];
                    break;

                case "Map_2":
                    clip = map_2_run[Random.Range(0, map_2_run.Length)];
                    break;
            }
        }
        if (!stop)
            StartCoroutine(playSound());  

        IEnumerator playSound() {
            stop = true;
            source.PlayOneShot(clip);
            // yield return new WaitForSeconds(clip.length); //ЗВУК ПО ДЛИНЕ КЛИПА 
            yield return new WaitForSeconds(timer); //ЗВУК ПО КОНСТАНТЕ
            stop = false;
        }
        


    }

    // Update is called once per frame
    void Update()
    {
        
    }
}
