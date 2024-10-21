// import React from 'react';
// import { GoogleLogin } from 'react-google-login';
// import axios from 'axios';

// const Login = () => {
//   const responseGoogle = (response) => {
//     axios.post('http://localhost:5000/login', {
//       token: response.tokenId,
//     }).then((res) => {
//       console.log(res.data);
//       window.location.href = "/video";
//     }).catch((error) => {
//       console.error(error);
//     });
//   }

//   return (
//     <div>
//       <GoogleLogin
//         clientId="YOUR_GOOGLE_CLIENT_ID"
//         buttonText="Login with Google"
//         onSuccess={responseGoogle}
//         onFailure={responseGoogle}
//         cookiePolicy={'single_host_origin'}
//       />
//     </div>
//   );
// }

// export default Login;
