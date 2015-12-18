var $form = $("#newItem"),
    $errorMsg = $("<span class='error' style='color:red'>This field is required..!!</span>"),
    $errorMsgRepeat = $("<span class='error' style='color:red'>This item already exits..!!</span>");


$("#submit").on("click", function () {
    // console.log('hello' + checkIsExit('Foosball','test'));
    var toReturn = true;
    $("#inputField", $form).each(function () {
         if ($(this).data("error")) {
            $(this).data("error").remove();
            $(this).removeData("error");
        }
        if ($(this).val() == "") {
            if (!$(this).data("error")) {
                $(this).data("error", $errorMsg.clone().insertAfter($(this)));
            }
            toReturn = false;
        }
        else {
            // toReturn = false;
            var checkUrl = '/check/' + $("#category").val() + '/' + $('#inputField').val();
            console.log(checkUrl);
            var isExist;

            $.ajax({
                type: "get",
                url: checkUrl,
                async: false,
                success: function(data) {
                    isExist = data.isExist;
                    console.log(isExist);
                }
            });
            if (isExist) {
                toReturn = false;
                $(this).data("error", $errorMsgRepeat.clone().insertAfter($(this)));
            }
           
        }
    });
    return toReturn;
});