function postjson()
{
    message = document.getElementsByTagName("textarea")[0].value;
    if (message){
        ajaxcall(jsondata(message));
    }
}

function jsondata(message)
{
    var obj = {};
    obj.message = message;
    // obj.csrfmiddlewaretoken = "{{ csrf_token }}";
    return obj;
}

function ajaxcall(json)
{
    $.ajax({
          type: "POST",
          url: window.location.href,
          data: JSON.stringify(json),
          dataType: "text",
    });
}