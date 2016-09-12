var drocer = {};
drocer.action = {};
drocer.callback = {};
drocer.ui = {};
drocer.settings = {};
drocer.settings.search_input_element = 'search-input';
drocer.settings.search_results_element = 'search-results';
drocer.settings.page_image_container = 'page-image-container';
drocer.settings.page_image_element = 'page-image';
drocer.settings.page_overlay_element = 'page-image-overlay';
drocer.settings.spinner = '<div class="preloader-wrapper big active"><div class="spinner-layer spinner-green-only"><div class="circle-clipper left"><div class="circle"></div></div><div class="gap-patch"><div class="circle"></div></div><div class="circle-clipper right"><div class="circle"></div></div></div></div>';
drocer.action.search = function(){
    var results_container = document.getElementById(drocer.settings.search_results_element);
    $(results_container).html(drocer.settings.spinner);
    $.post(
        './search',
        {q: $('#'+drocer.settings.search_input_element).val()},
        drocer.callback.search,
        'json'
    );
};
drocer.callback.search = function(response){
    window.DEBUG_SEARCH = response;//debug
    if(response.length > 0){
        drocer.ui.render_search_results(response);
    } else {
        $(document.getElementById(drocer.settings.search_results_element)).html('No results.');
    }
};
drocer.ui.render_search_results = function(results){
    var results_container = document.getElementById(drocer.settings.search_results_element);
    var ul = document.createElement('ul');
    ul.className= 'collection';
    for(var r in results){
        var result = results[r];
        // create collection item
        var li = document.createElement('li');
        li.className = 'collection-item';
        ul.appendChild(li);
        // create collection item title
        var span = document.createElement('span');
        span.className = 'title';
        span.style = 'font-weight: bold;'
        var txt = document.createTextNode(result.title);
        span.appendChild(txt);
        li.appendChild(span);
        // create collection item lines
        var counter = 1;
        for(var b in result.boxes){
            var box = result.boxes[b];
            var p = document.createElement('p');
            var txt = document.createTextNode('Page '+box.page_number);
            var a = document.createElement('a');
            a.href = '#';
            a.title = box.text;
            a.setAttribute('data-drocer-box', JSON.stringify(box));
            a.setAttribute('data-drocer-document-name', JSON.stringify(result.document_name));
            a.onclick = function(){
                // load page image
                var document_name = JSON.parse(this.getAttribute('data-drocer-document-name'));
                var box = JSON.parse(this.getAttribute('data-drocer-box'));
                var page_image_url = './page_images/'+document_name+'-'+box.page_number+'.png';
                var page_image = new Image();
                page_image.onload = function(){
                    // position overlay on match box
                    var ov = document.getElementById('page-image-overlay');
                    page_box = drocer.ui.box_to_page(box);
                    ov.style.height = page_box.height+'px';
                    ov.style.width = page_box.width+'px';
                    ov.style.top = page_box.top+'px';
                    ov.style.left = page_box.left+'px';
                    window.DEBUG_PAGE_BOX = page_box;
                    var scroll_x = page_box.left - 325;
                    var scroll_y = page_box.top - 25;
                    console.log('scrolling: window.scrollTo('+scroll_x+','+scroll_y+')');
                    window.scrollTo(scroll_x, scroll_y);
                }
                page_image.src = page_image_url;
                page_image.id = drocer.settings.page_image_element;
                page_image.style.zIndex = 900;
                var page_image_container = document.getElementById(drocer.settings.page_image_container);
                $(page_image_container).html(page_image);
                window.DEBUG_BOX = box;
            };
            p.appendChild(txt);
            a.appendChild(p);
            li.appendChild(a);
            counter++;
        }
    }
    $(results_container).html(ul);
};
drocer.ui.box_to_page = function(box){
    window.scrollTo(0,0);
    var body_rect = document.body.getBoundingClientRect()
    // images are 1466x1903
    var img_rect = document.getElementById('page-image').getBoundingClientRect();
    //var x_scale = img_rect.width / 800;
    //var y_scale = img_rect.height / 800;
    var x_scale = 175 / 72;
    var y_scale = 175 / 72; // convert dpi / source dpi
    function page_x(x){
        return img_rect.left + body_rect.left + x * x_scale;
    }
    function page_y(y){
        return body_rect.top + img_rect.top + img_rect.height - y * y_scale;
    }
    return {
        top: page_y(box.y1),
        left: page_x(box.x0),
        height: page_y(box.y0) - page_y(box.y1),
        width: page_x(box.x1) - page_x(box.x0)
    }
};
