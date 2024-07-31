function fetchSwitches(base) {
    fetch('/get_flows', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `base=${encodeURIComponent(base)}`
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);  // 在浏览器控制台打印返回的数据
        displayDataAsTable(data);  // 调用函数显示数据为表格
    })
    .catch(error => console.error('Error:', error));
}   

function displayDataAsTable(data) {       
    let pattern = /\,/;  
    var table = '<table id="sortableTable"><tr>\
        <th onclick="sortTable(0)">DIPD</th>\
        <th onclick="sortTable(1)">cookie</th>\
        <th onclick="sortTable(2)">table</th>\
        <th onclick="sortTable(3)">priority</th>\
        <th onclick="sortTable(4)">match</th>\
        <th onclick="sortTable(5)">action</th></tr>';
    data.forEach(switchInfo => {
        switchInfo.flows.forEach(flow => {
            let matchedKeys = Object.keys(flow).filter(key => pattern.test(key));
            if (flow[matchedKeys] === undefined) {
                var match = ''
            } else {
                var match = `${matchedKeys}=${flow[matchedKeys]}`
            }
            table += `<tr>
                        <td>${switchInfo.dpid}</td>
                        <td>${flow.cookie}</td>
                        <td>${flow.table}</td>
                        <td>${flow.priority}</td>
                        <td>${match}</td>
                        <td>${flow.actions}</td>
                      </tr>`;
        });
    });
    table += '</table>';
    document.getElementById('results').innerHTML = table;  
}

function sortTable(column) {
    var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
    table = document.getElementById("sortableTable");
    switching = true;
    // 设置排序方向为升序
    dir = "asc";
    // 使循环直到没有需要交换的行为止
    while (switching) {
        switching = false;
        rows = table.rows;
        // 遍历所有表格行（除了标题）
        for (i = 1; i < (rows.length - 1); i++) {
            shouldSwitch = false;
            // 比较两个相邻行的列数据
            x = rows[i].getElementsByTagName("TD")[column];
            y = rows[i + 1].getElementsByTagName("TD")[column];
            // 根据方向适当地检查是否需要交换
            if (dir == "asc") {
                if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
                    // 如果是升序，且前面的大于后面的，标记为需要交换
                    shouldSwitch = true;
                    break;
                }
            } else if (dir == "desc") {
                if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
                    // 如果是降序，且前面的小于后面的，标记为需要交换
                    shouldSwitch = true;
                    break;
                }
            }
        }
        if (shouldSwitch) {
            // 如果标记为需要交换，则执行交换并标记开关为打开
            rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
            switching = true;
            switchcount++;
        } else {
            // 如果在一轮中没有交换，且方向为升序，则改为降序，再做一次循环
            if (switchcount == 0 && dir == "asc") {
                dir = "desc";
                switching = true;
            }
        }
    }
}

