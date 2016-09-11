var drocer = {};
drocer.action = {};
drocer.callback = {};
drocer.action.search = function(){
    $.post('./search', {q: $('#search').val()});
};
drocer.callback.search = function(response){
    window.DEBUG_SEARCH = response;//debug
};
