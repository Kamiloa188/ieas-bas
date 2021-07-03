from controllers import registrousercontrollers
user = {
    
    "registro_user": "/api/v01/user/registro", "registro_user_controllers": registrousercontrollers.as_view("registro_api"),
}
#"datos_user": "/api/v01/user/datos", "datos_user_controllers": datosUserControllers.as_view("datos_api"),