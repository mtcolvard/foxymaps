import React from 'react'
import ReactDOM from 'react-dom'
import {BrowserRouter, Routes, Route} from 'react-router-dom'
import { library } from '@fortawesome/fontawesome-svg-core'
import { faArrowLeft, faTimes, faDirections, faLocationArrow, faMapMarkerAlt, faArrowsAltV } from '@fortawesome/free-solid-svg-icons'
library.add(faArrowLeft, faTimes, faDirections, faLocationArrow, faMapMarkerAlt, faArrowsAltV)

import './scss/style.scss'
import Map from './components/Map'

class App extends React.Component {

  render () {
    return(
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Map />} />
        </Routes>
      </BrowserRouter>
    )
  }
}

ReactDOM.render(
  <App />,
  document.getElementById('root')
)

// react-router-5 config
// render () {
//   return(
//     <HashRouter>
//       <Switch>
//         <Route path="/" component={Map} />
//       </Switch>
//     </HashRouter>
//   )
// }
// }
