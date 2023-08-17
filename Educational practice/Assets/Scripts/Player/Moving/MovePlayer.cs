using System.Collections;
using System.Collections.Generic;
using UnityEngine;

//НЕОБХОДИМОСТЬ КОМПОНЕТА ДЛЯ РАБОТЫ СКРИПТА
[RequireComponent(typeof(CharacterController))]

//СКРИПТ ДЛЯ ХОДЬБЫ
public class MovePlayer : MonoBehaviour {

    public float speed;
    private PlayerSoundsWalk playsoundswalk;
    private CharacterController _charController;
    [HideInInspector]public bool Run_Player;
 
    // Start is called before the first frame update
    void Start()
    {
        _charController = GetComponent<CharacterController>();
        playsoundswalk = GetComponent<PlayerSoundsWalk>();
    }

    // Update is called once per frame
    void Update()
    {
        float posZ = Input.GetAxis("Vertical") * speed * Time.deltaTime; //кнопики A = 1, D = - 1
        float posX = Input.GetAxis("Horizontal") * speed * Time.deltaTime; //кнопики W = 1, S = - 1
        Vector3 move = new Vector3(posX, -9.8f, posZ);
        move = Vector3.ClampMagnitude(move, speed);
        move = transform.TransformDirection(move);

        _charController.Move(move);
        
        //ЛУЧ ДЛЯ ПРОВЕРКИ ПОВЕРХНОСТИ
        Debug.DrawRay(transform.position, Vector3.down, Color.red);

        if(posX != 0 || posZ != 0) {
            Ray ray = new Ray(transform.position, Vector3.down);
            RaycastHit hit;

            run_Player();

            if (Physics.Raycast(ray, out hit))
                playsoundswalk.PlayStep(hit.collider.name);
        }
    }

    private void run_Player() {
        if (Input.GetKey(KeyCode.LeftShift)) {
                speed = 8;
                Run_Player = true;
        }   else {
                speed = 5;
                Run_Player = false;
        } 
    }
}
