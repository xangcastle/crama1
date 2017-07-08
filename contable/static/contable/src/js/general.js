var recargar ;

$(document).ready(function()
{
    $(document).on("submit",".form_entrada",function(e)
    {
       e.preventDefault();
       if(validar_campos_vacios())
         return ;
       var formu=$(this);
       var url=$(this).attr("action");
             $.ajax({
                       type: "POST",
                       url : url,
                       datatype:'json',
                       data : formu.serialize(),
                       success : function(e)
                       {
                         if(typeof(e.error) != "undefined")
                             swal('Error',e.error,'error');
                         else
                         {
                           recargar = setTimeout(recargar_pagina, 1000);
                           swal('Acción Exitosa',e.result,'success');
                         }
                       },error : function(data)
                       {
                         swal
                         (
                           'Error',
                           data.responseText,
                           'error'
                         );
                       }
                     });
    });

    $(document).on("submit",".form_archivo",function(e)
    {
       e.preventDefault();
       if(validar_campos_vacios())
         return ;
       var formu=$(this);
       var url=$(this).attr("id");
       var formData = new FormData($("#"+url+"")[0]);
       var url=$(this).attr("action");
             $.ajax({
                       type: "POST",
                       url : url,
                       cache: false,
                       contentType: false,
                       processData: false,
                       data : formData,
                       success : function(e)
                       {
                         if(typeof(e.error)!= undefined)
                             swal('Error',e.error,'error');
                         else
                         {
                           recargar = setTimeout(recargar_pagina, 1000);
                            swal('Acción Exitosa',e.result,'success');
                         }

                       },error : function(data)
                       {
                         swal
                         (
                           'Error',
                           data.responseText,
                           'error'
                         );
                       }
                     });
    });




    $(document).on("submit",".form_login",function(e)
    {
       e.preventDefault();
       var form=$(this);
       var error = false;

       var username     = $('#username');
       var password     = $('#password');

       if (username.val().length == 0) {
          error = true;
         username.css("border-color", "#D8000C");
       } else {
         username.css("border-color", "#666");
       }

       if (password.val().length == 0) {
          error = true;
         password.css("border-color", "#D8000C");
       } else {
         password.css("border-color", "#666");
       }

       if (error == false)
       {
         this.submit();
       }
    });


    $(document).on("submit",".form_registro",function(e)
    {
       e.preventDefault();
       var form=$(this);
       var error = false;

       var empresa     = $('#empresa');
       var ruc         = $('#ruc');
       var username    = $('#username');
       var password    = $('#password');
       var email       = $('#email');

       if (empresa.val().length == 0) {
          error = true;
         empresa.css("border-color", "#D8000C");
       } else {
         empresa.css("border-color", "#666");
       }

       if (ruc.val().length == 0) {
          error = true;
         ruc.css("border-color", "#D8000C");
       } else {
         ruc.css("border-color", "#666");
       }

       if (username.val().length == 0) {
          error = true;
         username.css("border-color", "#D8000C");
       } else {
         username.css("border-color", "#666");
       }

       if (password.val().length == 0) {
          error = true;
         password.css("border-color", "#D8000C");
       } else {
         password.css("border-color", "#666");
       }

       if (email.val().length == 0) {
          error = true;
         email.css("border-color", "#D8000C");
       } else {
         email.css("border-color", "#666");
       }

       if (error == false)
       {
         this.submit();
       }

    });

    function recargar_pagina()
    {
      location.reload();
      clearTimeout(recargar);
    }

    function validar_campos_vacios()
    {
      var elementos = $(".requerido");
      var error = false ;
      $(".requerido").each(function(){
            if (this.value.length == 0) {
               error = true;
              $(this).css("border-color", "#D8000C");
            } else {
              $(this).css("border-color", "#666");
            }
        });
      return error;
    }





});
