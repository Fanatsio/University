//https://youtu.be/w9JV1R_VyOs
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class NoMouse : MonoBehaviour
{
    bool isLocked;
    // Start is called before the first frame update
    void Start() {
        SetCursorLock (true);
    }

    void SetCursorLock(bool isLocked) {
        this.isLocked = isLocked;
        Screen.lockCursor = isLocked;
        Cursor.visible = !isLocked;

    }

    // Update is called once per frame
    void Update(){
        if (Input.GetKeyDown (KeyCode.Tab))
            SetCursorLock (!isLocked);
    }
}
