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
    abilility_list = all_list[6];
    ind_list_suit = all_list[3];
    msa_list_suit = all_list[4];
    suit_final = all_list[5];

    t = {};
    abilility_list.forEach(function (k, i) {
        t[k] = skill_list[i+14]["skill_code"];
    });

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
        var ind_selected = $('#ind_list option:selected').text().split(' : ')[0];
        get_loss_values_ZCTA(ind_selected, "industry_loss");
        get_loss_values_MSA(ind_selected, "industry_loss");
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
        var occ_selected = $('#occ_list option:selected').text().split(' : ')[0];
        get_loss_values_ZCTA(occ_selected, "occupation_loss");
        get_loss_values_MSA(occ_selected, "occupation_loss");
    });

    var str1 = '';
    skill_list.forEach(function (t) { str1 += "<option>" + t.skill_code + " : " + t.skill_name + "</option>"; });
    $('#skill_list_complete').html(str1);
    $('#skill_list_complete').change(function() {
        var skill_selected = $('#skill_list_complete option:selected').text().split(' : ')[0];
        get_MSA_skill_values("LV", skill_selected);
        get_ZCTA_skill_values("LV", skill_selected);

        // console.log(skill_selected);
    });

    var str1 = '';
    skill_list.forEach(function (t) { str1 += "<option>" + t.skill_code + " : " + t.skill_name + "</option>"; });
    $('#skill_list_loss').html(str1);
    $('#skill_list_loss').change(function() {
        var skill_selected = $('#skill_list_loss option:selected').text().split(' : ')[0];
        get_loss_values_ZCTA(skill_selected, "skill_loss");
        get_loss_values_MSA(skill_selected, "skill_loss");
    });

    var str1 = '';
    abilility_list.forEach(function (t) { str1 += "<option>" + t + "</option>"; });
    $('#ability_list_complete').html(str1);
    $('#ability_list_complete').change(function() {
        var ability_selected = $('#ability_list_complete option:selected').text().split(' : ')[0];
        var skill_selected = t[ability_selected];
        get_MSA_skill_values("LV", skill_selected);
        get_ZCTA_skill_values("LV", skill_selected);
    });

    var str1 = '';
    ind_list_suit.forEach(function (t) {
       str1 +=  "<option>" + t + "</option>";
    });
    $('#suit_').html(str1);
    $('#suit_').change(function() {
        var ind_selected = $('#suit_ option:selected').text().split(' : ')[0];
        get_suit_MSA(ind_selected);
    });
}

function set_brew_scale(mapx) {
    var brew_map_new = new classyBrew();
    var final_range = [];
    for(var i = 0; i < mapx["features"].length; i ++) {
        if(mapx["features"][i].properties !== undefined){
            if (mapx["features"][i].properties.display !== undefined){
                if(mapx["features"][i].properties.display !== -1) {
                    final_range.push(mapx["features"][i].properties.display);
                }
            }
        }
    }
    brew_map_new.setSeries(final_range);
    brew_map_new.setNumClasses(6);
    brew_map_new.setColorCode("OrRd");
    brew_map_new.classify('equal_interval');
    // console.log(brew_map_new.getBreaks());
    return brew_map_new;
}