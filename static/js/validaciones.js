jQuery.validator.addMethod("nacimiento", function(value, element) {
    var fechaNacimiento = new Date(value);
    var fechaActual = new Date();
    return fechaNacimiento < fechaActual;
}, "La fecha de nacimiento debe ser menor que la fecha actual");

$("#frmRegistro").validate({
    debug: true,
    errorClass: "errorMessage",
    rules:{
        inputName:{
            required: true,
            minlength: 2
        },
        inputApellido:{
            required: true,
            minlength: 2
        },
        inputEmail: {
            required: true,
            email: true
        },
        inputReEmail: {
            equalTo: "#inputEmail"
        },
        inputPass: {
            required: true,
            minlength: 8
        },
        inputRePass: {
            equalTo: "#inputPass"
        },
        inputTelefono: {
            required: true,
            minlength: 8
        },
        inputDir:{
            required: true,
            minlength: 8
        },
        inputPais: {
            required: true
        },
        inputCiudad: {
            required: true
        },
        inputComuna: {
            required: true
        },
        inputFechaNac: {
            required: true,
            date: true,
            nacimiento: true
        },
        checkTerms: {
            required: true
        }

    },
    messages: {
        inputName: {
            required: "El campo nombre no puede estar vacio.",
            minlength: jQuery.validator.format("El campo nombre debe tener como minimo 2 caracteres.")
        },
        inputApellido: {
            required: "El campo apellido no puede estar vacio.",
            minlength: jQuery.validator.format("El campo apellido debe tener un minimo de 2 caracteres."),
        },
        inputEmail: {
            required: "El campo email no puede estar vacio.",
            email: jQuery.validator.format("El campo email debe tener formato correo."),
        },
        inputReEmail: {
            equalTo: "El email debe coincidir"
        },
        inputPass: {
            required: "La contraseña no puede estar vacia.",
            minlength: jQuery.validator.format("La contraseña debe tener un minimo de 8 caracteres."),
        },
        inputRePass: {
            equalTo: "La contraseña debe coincidir"
        },
        inputTelefono: {
            required: "El teléfono no puede estar vacio",
            minlength: jQuery.validator.format("El teléfono debe tener un minimo de 8 números."),
        },
        inputDir:{
            required: "La dirección no puede estar vacia",
            minlength: jQuery.validator.format("La dirección debe tener un minimo de 8 caracteres."),
        },
        inputPais: {
            required: "Debe seleccionar un país del listado"
        },
        inputCiudad: {
            required: "La ciudad no puede estar vacia"
        },
        inputComuna: {
            required: "La comuna no puede estar vacia"
        },
        inputFechaNac: {
            required: "Debe seleccionar su fecha de nacimiento",
            date: true,
            nacimiento: true
        },
        checkTerms: {
            required: "Debe aceptar los términos y condiciones"
        }
    }
}),

$("#frmContacto").validate({
    debug: true,
    errorClass: "errorMessage",
    rules:{
        inputName:{
            required: true,
            minlength: 5
        },
        inputPais: {
            required: true
        },
        inputRUNDNI: {
            required: true,
            minlength: 6
        },
        inputTelefono: {
            required: true,
            minlength: 8
        },
        inputEmail: {
            required: true,
            email: true
        },
        inputMensaje: {
            required: true,
            minlength: 30
        }

    },
    messages: {
        inputName: {
            required: "El campo nombre no puede estar vacio.",
            minlength: jQuery.validator.format("El campo nombre debe tener como minimo 5 caracteres.")
        },
        inputPais: {
            required: "Debe seleccionar un país del listado"
        },
        inputRUNDNI: {
            required: "Debe ingresar un RUN o DNI de identificación personal",
            minlength: "El RUN o DNI debe ser de mínimo 5 caracteres"
        },
        inputTelefono: {
            required: "El teléfono no puede estar vacio",
            minlength: jQuery.validator.format("El teléfono debe tener un minimo de 8 números."),
        },
        inputEmail: {
            required: "El campo email no puede estar vacio.",
            email: jQuery.validator.format("El campo email debe tener formato correo."),
        },
        inputMensaje: {
            required: "Por favor, escriba un mensaje para contactarnos",
            minlength: jQuery.validator.format("El mensaje debe tener mínimo 30 caracteres."),
        }
    }
});