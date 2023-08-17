using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CursorHand : MonoBehaviour
{
    public bool cursorEnter = false;
    public Texture2D cursorTexture_Main;
    public Texture2D cursorTexture_Hand;
    public float distance = 1;
    public bool dist = false;

    void Start() {
        cursorEnter = false;
        dist = false;
    }

    // Update is called once per frame
    void Update()
    {
        GameObject player = GameObject.FindGameObjectWithTag("Player");
        
        if (cursorEnter == true){
            if (Vector3.Distance(transform.position, player.transform.position) <= distance)
                dist = true;
            else 
                dist = false;
        }
    }

    void OnMouseEnter() {
        cursorEnter = true;
    }

    void OnMouseExit() {
        cursorEnter = false;
    }

    void OnGUI() {
        if (dist == true && cursorEnter == true)
            GUI.DrawTexture(new Rect(Screen.width/2-40, Screen.height/2-30, 80, 60), cursorTexture_Hand);
        else 
            GUI.DrawTexture(new Rect(Screen.width/2-40, Screen.height/2-30, 80, 60), cursorTexture_Main);
    }
}
