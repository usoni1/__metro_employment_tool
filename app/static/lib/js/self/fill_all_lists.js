$(document).ready(
    function () {
        var abilities = ['Category Flexibility ','Deductive Reasoning' ,'Flexibility of Closure' ,'Fluency of Ideas','Inductive Reasoning' ,'Information Ordering' ,'Mathematical Reasoning' ,'Memorization' ,'Number Facility', 'Oral Comprehension' ,'Oral Expression' ,'Originality' ,'Perceptual Speed' ,'Problem Sensitivity' ,'Selective Attention' ,'Spatial Orientation Speed of Closure' ,'Time Sharing' ,'Visualization' ,'Written Comprehension' ,'Written Expression'];

        var xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function () {
            if(this.readyState === 4 && this.status === 200) {
                all_list = JSON.parse(this.responseText);
                all_list.push(abilities);
                $("input[name='occ_level']:radio").change(set_all_lists);
                $("input[name='industry_level']:radio").change(set_all_lists);
                set_all_lists();
            }
        };
        xhr.open('GET', '/get_all_lists');
        xhr.send();

    }
);

function set_all_lists() {
    custom_range = [0, 0];
    // console.log(all_list);
    selected_occ_level = $("input[name='occ_level']:checked").val();
    selected_industry_level = $("input[name='industry_level']:checked").val();
    occ_list = all_list[0];
    ind_list = all_list[1];
    skill_list = all_list[2];
    abilility_list = all_list[3];

    var str1 = '';
    ind_list.
    filter(
        function (t) {
            var t1 = t.ind_code.replace(/0*$/, '');
            return t1.length === parseInt(selected_industry_level);
        }
    ).
    forEach(
        function (t) { str1 += "<option>" + t.ind_code + " : " + t.ind_title + "</option>"; }
    );
    $('#ind_list').html(str1);
    $('#ind_list').change(function() {
        custom_range = [0, 10];
        set_brew_scale();
        update_main_map();
    });

    str1 = '';
    occ_list
        .filter(
            function(t){
                var t1 = t.occ_code.replace(/0*$/, '');
                return t1.length === parseInt(selected_occ_level);
        }
        ).forEach(
            function (t) { str1 += "<option>" + t.occ_code + " : " + t.occ_name + "</option>"; }
        );

    $('#occ_list').html(str1);
    $('#occ_list').change(function() {
        custom_range = [0, 10];
        set_brew_scale();
        update_main_map();
    });

    var str1 = '';
    skill_list.forEach(function (t) { str1 += "<option>" + t.skill_code + " : " + t.skill_name + "</option>"; });
    $('#skill_list_complete').html(str1);
    $('#skill_list_complete').change(function() {
        custom_range = [0, 5];
        set_brew_scale();
        update_main_map();
    });

    var str1 = '';
    skill_list.forEach(function (t) { str1 += "<option>" + t.skill_code + " : " + t.skill_name + "</option>"; });
    $('#skill_list_loss').html(str1);
    $('#skill_list_loss').change(function() {
        custom_range = [0, 5];
        set_brew_scale();
        update_main_map();
    });

    var str1 = '';
    abilility_list.forEach(function (t) { str1 += "<option>" + t + "</option>"; });
    $('#ability_list_complete').html(str1);
    $('#ability_list_complete').change(function() {
        custom_range = [0, 5];
        set_brew_scale();
        update_main_map();
    });
}

function set_brew_scale() {
    brew_map = new classyBrew();
    brew_map.setSeries(custom_range);
    brew_map.setNumClasses(5);
    brew_map.setColorCode("BuGn");
    brew_map.classify('equal_interval');
    console.log(brew_map.getBreaks());
}