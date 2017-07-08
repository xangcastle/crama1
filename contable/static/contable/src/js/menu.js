
$(document).ready(function()
{
  $('.child_menu li').click(function ()
    {
       redireccionar_menu(this);
    });

  $('.item_menu').click(function ()
    {
       redireccionar_menu(this);
    });

    function redireccionar_menu(obj)
    {
        var url = $(obj).attr('rel');
        if(typeof(url) == "undefined")
            return ;
        $.get(url,function(resul)
        {
          $("#contenido_principal").html(resul);
        })
        .fail(function(data)
           {
                swal
                (
                  'Error',
                  data.responseText,
                  'error'
                );
            });

        var li ;
        for($('.child_menu li') in li )
        {
            if(li != obj)
              $(obj).attr('class', "");
            else
              $(obj).attr('class', "current-page");
        }
    }
});
