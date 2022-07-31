import React, { useEffect, useState } from 'react';
export default function getProducts(callback) {
  fetch('https://wzoujjhpbc.execute-api.ap-southeast-2.amazonaws.com/dev/groceries/products')
    .then(response => response.json())
    .then(json_data => {
      json_data.sort((a,b) => a.category.localeCompare(b.category));
      callback(json_data);
    });

}
