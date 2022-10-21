import getRestApiBaseUrl from './config';

export default function getProducts(callback) {
  fetch(`${getRestApiBaseUrl()}/groceries/products`)
    .then(response => response.json())
    .then(json_data => {
      console.log(json_data);
      callback(json_data);
    });

}
