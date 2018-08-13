function get_MSA_skill_values(skill_type, skill_code) {
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () {
        if(this.readyState === 4 && this.status === 200) {
            var value_range = [];
            var msa_skill_arr = JSON.parse(this.responseText);
            // console.log(msa_skill_arr);
            msa_skill_values = {};
            msa_skill_arr.forEach(function (d) {
                msa_skill_values[d[0]] = d[1];
                value_range.push(d[1]);
            });

            metro_data["features"].forEach(function (t) {
               msa_id = t.properties.GEOID;
               if(msa_skill_values[msa_id] === undefined) {
                   t.properties.display = -1;
                   return;
               }
               t.properties.display = msa_skill_values[msa_id];
            });
            brew_map2 = set_brew_scale(metro_data);
            update_main_map2(brew_map2);
        }
    };
    xhr.open('GET', '/get_all_msa_skill?skill_type='+skill_type+'&skill_code='+skill_code);
    xhr.send();
}

function get_ZCTA_skill_values(skill_type, skill_code) {
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () {
        if(this.readyState === 4 && this.status === 200) {
            var value_range_ZCTA = [];
            zcta_skill_arr = JSON.parse(this.responseText);
            // console.log(zcta_skill_arr);
            zcta_skill_values = {};
            zcta_skill_arr.forEach(function (d) {
                zcta_skill_values[d[0]] = d[1];
                if (d[1] !== "-1"){
                    value_range_ZCTA.push(d[1]);
                }

            });

            az_map["features"].forEach(function (t) {
               zcta_id = t.properties.ZCTA_ID;
               zcta_id = zcta_id.slice(1);

               t.properties.display = zcta_skill_values[zcta_id];
            });

            var brew_map1 = set_brew_scale(az_map);
            update_main_map1(brew_map1);
        }
    };
    xhr.open('GET', '/get_all_zcta_skill?skill_type='+skill_type+'&skill_code='+skill_code);
    xhr.send();
}

function get_loss_values_ZCTA(loss_holder, loss_type) {
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () {
        if(this.readyState === 4 && this.status === 200) {
            value_range_ZCTA_loss = [];
            var zcta_loss_arr = JSON.parse(this.responseText);
            zcta_loss = {};
            zcta_loss_arr.forEach(function (d) {
                zcta_loss[d.zcta_id] = d.display;
                value_range_ZCTA_loss.push(d.display);
            });
            // TODO industries have different number of respondents per ZCTA can't use the same base map anymore, change it
            az_map["features"].forEach(function (t) {
               zcta_id = t.properties.ZCTA_ID;
               t.properties.display = zcta_loss[zcta_id];
            });
            var brew_map3 = set_brew_scale(az_map);
            update_main_map1(brew_map3);
        }
    };
    xhr.open('GET', '/get_zcta_loss_stats?loss_holder='+loss_holder+'&loss_type='+loss_type);
    xhr.send();
}

function get_loss_values_MSA(loss_holder, loss_type) {
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () {
        if(this.readyState === 4 && this.status === 200) {
            value_range_ZCTA_loss = [];
            var zcta_loss_arr = JSON.parse(this.responseText);
            zcta_loss = {};
            zcta_loss_arr.forEach(function (d) {
                zcta_loss[d.msa_id] = d.display;
                value_range_ZCTA_loss.push(d.display);
            });
            // TODO industries have different number of respondents per ZCTA can't use the same base map anymore, change it
            metro_data["features"].forEach(function (t) {
               zcta_id = t.properties.GEOID;
               t.properties.display = zcta_loss[zcta_id];
            });
            var brew_map3 = set_brew_scale(metro_data);
            update_main_map2(brew_map3);
        }
    };
    xhr.open('GET', '/get_msa_loss_stats?loss_holder='+loss_holder+'&loss_type='+loss_type);
    xhr.send();
}

function get_suit_MSA(ind_selected){
    ind_idx = null;
    ind_selected = parseInt(ind_selected);
    ind_list_suit.forEach(function (t, i) {
       if(t === ind_selected) {
           console.log(t);
           ind_idx = i;
       }
    });

    suit_map = {};
    console.log(ind_idx);
    msa_list_suit.forEach(function (msa, idx) {
        suit_map[msa] = parseFloat(suit_final[idx][ind_idx]);
    });

    metro_data["features"].forEach(function (t) {
       msa_id = t.properties.GEOID;
       if(msa_id in suit_map){
           t.properties.display = suit_map[msa_id];
       } else {
           t.properties.display = -1;
       }
    });

    brew_map_suit = set_brew_scale(metro_data);
    update_main_map2(brew_map_suit);
}

function populate_occ_rank_list(zcta_id) {
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () {
        if(this.readyState === 4 && this.status === 200) {
            occ_rank_list = JSON.parse(this.responseText);
            occ_rank_list = occ_rank_list.slice(1, 100);
            var t1 = $("#top_occ_loss tbody");
            var str1 = '';
            occ_rank_list.forEach(function (t, idx) {
                str1 = str1 +
                '<tr>' +
                '<td>'+ (idx + 1) + '</td>' +
                '<td>' + t[0] + '</td>' +
                '<td>' + t[0] + '</td>' +
                '<td>' + t[1] + '</td>' +
                '</tr>';
            });
            t1.html(str1);
        }
    };
    xhr.open('GET', '/get_zcta_loss_rank_stats?zcta_id='+zcta_id+'&loss_type=occ_loss');
    xhr.send();
}

function populate_ind_rank_list(zcta_id) {
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () {
        if(this.readyState === 4 && this.status === 200) {
            occ_rank_list = JSON.parse(this.responseText);
            occ_rank_list = occ_rank_list.slice(1, 100);
            var t1 = $("#top_ind_loss tbody");
            var str1 = '';
            occ_rank_list.forEach(function (t, idx) {
                str1 = str1 +
                '<tr>' +
                '<td>'+ (idx + 1) + '</td>' +
                '<td>' + t[0] + '</td>' +
                '<td>' + t[0] + '</td>' +
                '<td>' + t[1] + '</td>' +
                '</tr>';
            });
            t1.html(str1);
        }
    };
    xhr.open('GET', '/get_zcta_loss_rank_stats?zcta_id='+zcta_id+'&loss_type=ind_loss');
    xhr.send();
}

function populate_skill_rank_list(zcta_id) {
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () {
        if(this.readyState === 4 && this.status === 200) {
            occ_rank_list = JSON.parse(this.responseText);
            occ_rank_list = occ_rank_list.slice(1, 100);
            var t1 = $("#top_skill_loss tbody");
            var str1 = '';
            occ_rank_list.forEach(function (t, idx) {
                str1 = str1 +
                '<tr>' +
                '<td>'+ (idx + 1) + '</td>' +
                '<td>' + t[0] + '</td>' +
                '<td>' + t[0] + '</td>' +
                '<td>' + t[1] + '</td>' +
                '</tr>';
            });
            t1.html(str1);
        }
    };
    xhr.open('GET', '/get_zcta_loss_rank_stats?zcta_id='+zcta_id+'&loss_type=skill_loss');
    xhr.send();
}

function populate_occ_rank_list_m(zcta_id) {
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () {
        if(this.readyState === 4 && this.status === 200) {
            occ_rank_list = JSON.parse(this.responseText);
            occ_rank_list = occ_rank_list.slice(1, 100);
            var t1 = $("#top_occ_loss tbody");
            var str1 = '';
            occ_rank_list.forEach(function (t, idx) {
                str1 = str1 +
                '<tr>' +
                '<td>'+ (idx + 1) + '</td>' +
                '<td>' + t[0] + '</td>' +
                '<td>' + t[0] + '</td>' +
                '<td>' + t[1] + '</td>' +
                '</tr>';
            });
            t1.html(str1);
        }
    };
    xhr.open('GET', '/get_msa_loss_rank_stats?msa_id='+zcta_id+'&loss_type=occ_loss');
    xhr.send();
}

function populate_ind_rank_list_m(zcta_id) {
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () {
        if(this.readyState === 4 && this.status === 200) {
            occ_rank_list = JSON.parse(this.responseText);
            occ_rank_list = occ_rank_list.slice(1, 100);
            var t1 = $("#top_ind_loss tbody");
            var str1 = '';
            occ_rank_list.forEach(function (t, idx) {
                str1 = str1 +
                '<tr>' +
                '<td>'+ (idx + 1) + '</td>' +
                '<td>' + t[0] + '</td>' +
                '<td>' + t[0] + '</td>' +
                '<td>' + t[1] + '</td>' +
                '</tr>';
            });
            t1.html(str1);
        }
    };
    xhr.open('GET', '/get_msa_loss_rank_stats?msa_id='+zcta_id+'&loss_type=ind_loss');
    xhr.send();
}

function populate_skill_rank_list_m(zcta_id) {
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () {
        if(this.readyState === 4 && this.status === 200) {
            occ_rank_list = JSON.parse(this.responseText);
            occ_rank_list = occ_rank_list.slice(1, 100);
            var t1 = $("#top_skill_loss tbody");
            var str1 = '';
            occ_rank_list.forEach(function (t, idx) {
                str1 = str1 +
                '<tr>' +
                '<td>'+ (idx + 1) + '</td>' +
                '<td>' + t[0] + '</td>' +
                '<td>' + t[0] + '</td>' +
                '<td>' + t[1] + '</td>' +
                '</tr>';
            });
            t1.html(str1);
        }
    };
    xhr.open('GET', '/get_msa_loss_rank_stats?msa_id='+zcta_id+'&loss_type=skill_loss');
    xhr.send();
}