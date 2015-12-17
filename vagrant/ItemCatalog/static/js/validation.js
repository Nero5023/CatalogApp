var $form = $("#newItem"),
    $errorMsg = $("<span class='error'>This field is required..!!</span>");
console.log($form)
$("#submit").on("click", function () {
    console.log('inthe function')
    var toReturn = true;
    $("#inputField", $form).each(function () {
        if ($(this).val() == "") {
            if (!$(this).data("error")) {
                $(this).data("error", $errorMsg.clone().insertAfter($(this)));
            }
            toReturn = false;
        }
        else {
            if ($(this).data("error")) {
                $(this).data("error").remove();
                $(this).removeData("error");
            }
        }
    });
    return toReturn;
});