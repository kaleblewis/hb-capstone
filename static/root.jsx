const Router = ReactRouterDOM.BrowserRouter;
const Route =  ReactRouterDOM.Route;
const Link =  ReactRouterDOM.Link;
const Prompt =  ReactRouterDOM.Prompt;
const Switch = ReactRouterDOM.Switch;
const Redirect = ReactRouterDOM.Redirect;
const useParams = ReactRouterDOM.useParams;
const useHistory = ReactRouterDOM.useHistory;
// same as the above but using destructing syntax 
// const { useHistory, useParams, Redirect, Switch, Prompt, Link, Route } = ReactRouterDOM;

function Homepage() {
  return <div>
    <LogIn /> 
    <Nav />
     </div>
}

function About() {
  return <div> A tiny react demo site </div>
}

function SearchBar() { 
  return (
  <div>
      <input type="search"></input>
  </div>
  )
}

function Search() {
  return (
      <div>  
      <Nav />
        Search for stuff 
        <SearchBar/>
      </div>
    )
}

function LogIn() { 

  const [email, setEmail] = React.useState('');
  const [password, setPassword] = React.useState('');

  function handleLogin(evt) {
    evt.preventDefault();
    // console.log((email)
    // console.log(password)

    const data = { 
      email: email,
      password: password
    }

    const options = {
      method: 'POST',
      body: JSON.stringify(data),
      headers: {
        'Content-Type': 'application/json'
      },
    }

    // const promise = fetch('/api/login', options)
    // promise.then((response => response.json()).then(data => console.log(data))
    // .then(data1 => console.log(data1))

    fetch('/api/login', options)
    .then(response => response.json())
    .then(data => {
      if (data === 'login successful') { 
        console.log(data)
        return  <Redirect  to="/profile" />
        // return(
        //   <div>
        //       <Profile />
        //   </div>
        //   )
      } else{ 
        alert(data)
      }
    })

  }

  function handleEmailChange(evt) {
    setEmail(evt.target.value)
  }

  function handlePasswordChange(evt) {
    let what_they_just_typed = evt.target.value 
    console.log(what_they_just_typed)
    setPassword(evt.target.value)
  }

  return (
    <div>
      <form onSubmit={handleLogin}>
        Username:
        <input value={email} onChange={handleEmailChange} type="email"></input>
        Password:
        <input value={password} onChange={handlePasswordChange} type="password"></input>
        <button onClick={this.onSubmit}>Login</button>
      </form>
    </div>
  )
}



function Profile() {
  return <div> 
    <Nav></Nav>

    {/* <h1> {{ user.fname }} </h1> */}

    <h2>account information:</h2>
{/* 
    <p><b>Username (email address):</b> {{ user.email }} </p>
    <p><b>Preferred name:</b> {{ user.fname }} </p>
    <p><b>Member since:</b>	{{ user.user_since.strftime('%B %Y') }} </p> */}

    
    </div>
}

function UserPreferences() {
  return <div> 
    <Nav></Nav>

    <h2>default search parameters:</h2>
{/* 
    <p><b>subtitles language(s):</b> {{ user.preferences[-1].subtitle }} </p>
    <p><b>audio language(s):</b>  {{ user.preferences[-1].audio }} </p>
    
    <p><b>release date range "from when?": </b> {{ user.preferences[-1].eyear }} </p>
    <p><b>release date range "to when?": </b> {{ user.preferences[-1].syear }} </p>

    <p><b>runtime/duration:</b>  {{ user.preferences[-1].duration }}  </p>

    <p><b>genre(s):</b>  {% for obj in user_genres %}
    {% for field in obj.__table__.columns._data.keys() %}
    {% if field == 'genre_name' %}
    {{ obj[field] }}<br>
    {% endif %}


    {% endfor %}
  {% endfor %}	
  </p>  

    <p><b>maturity rating:</b>  { user.preferences[-1].matlevel } 	</p>

    <p><b>viewing location:</b>  { user.preferences[-1].location.name } 	</p>
    <br>
    <hr>
    */}
    </div> 
}


function Recommendations() {
  return <div>
    <Nav></Nav>
    User's recommendations screen </div>
}


function Title() {
  return <div> 
    <Nav></Nav>
    Results for full details of a given titleID </div>
}


function Actor() {
  return <div> 
    <Nav></Nav>
    Results for available titles for a given actor </div>
}


function Nav() {
  return (
  <div>        
    <nav>
      <ul>
        <li>
            <Link to="/"> Home </Link>
        </li>
        <li>
            <Link to="/search"> Search </Link>
        </li>
        <li>
            <Link to="/profile"> Profile </Link>
        </li>
      </ul>
    </nav>
  </div>
  )
}

function App() {
    return (
      <Router>
        <div>
          <Switch>
            <Route path="/about">
              <About />
            </Route>
            <Route path="/login">
              <LogIn />
            </Route>
            <Route path="/profile">
              <Profile />
            </Route>
            <Route path="/search">
              <Search />
            </Route>
            <Route path="/recommendations">
              <Recommendations />
            </Route>
            <Route path="/title">
              <Title />
            </Route>
            <Route path="/actor">
              <Actor />
            </Route>
            <Route path="/">
              <Homepage />
            </Route>
          </Switch>
        </div>
      </Router>
    );
}

ReactDOM.render(<App />, document.getElementById('root'))

