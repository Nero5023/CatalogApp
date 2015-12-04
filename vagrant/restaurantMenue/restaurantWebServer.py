from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
import restaurantCURD

class WebserverHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		try:
			if self.path.endswith('/edit'):
				restaurantID = self.path.split("/")[2]
				restaurant = restaurantCURD.restaurantWithID(restaurantID)
				if restaurant:
					self.send_response(200)
					self.send_header('Content-type', 'text/html')
					self.end_headers()
					output = ""
					output += "<html><body>"
					output += "<h1>"
					output += restaurant.name
					output += "</h1>"
					output += r'''<form method='POST' enctype='multipart/form-data' 
											action = '/restaurant/%s/edit'>''' % restaurantID
					output += "<input name = 'newRestaurantName' type='text' placeholder = '%s'>" %restaurant.name
					output += "<input type = 'submit' value = 'Rename'>"
					output += "</form>"
					output += "</body></html>"

					self.wfile.write(output)

			if self.path.endswith('/delete'):
				restaurantID = self.path.split("/")[2]
				restaurant = restaurantCURD.restaurantWithID(restaurantID)
				if restaurant:
					self.send_response(200)
					self.send_header('Content-type', 'text/html')
					self.end_headers()
					output = ""
					output += "<html><body>"
					output += "<h1> Do you want to Delete %s ?</h1>" % restaurant.name
					output += r'''<form method='POST' enctype = 'multipart/form-data'
										action = '/restaurant/%s/delete' >''' % restaurantID
					output += "<input type='submit' value = 'Delete'>"
					output += "</form>"
					output += "</body></html>"

					self.wfile.write(output)


			if self.path.endswith("/restaurants"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				
				output = ""
				output += r'''<!DOCTYPE html>
				<html><head><title></title></head><body>'''
				output += "<h1><a href='/restaurants/new'>Make a New Restaurant Here</a></h1>"
				for restaurant in restaurantCURD.listAllRestaurant():
					output += r'''
					<div>
						<h1> %s </h1>
						<a href ="/restaurants/%s/edit">Edit</a>
						</br>
						<a href ="/restaurants/%s/delete">Delete</a>
						</br></br></br>
					</div>''' % (restaurant.name, restaurant.id, restaurant.id)
				output += "</body></html>"
				self.wfile.write(output)
				print output
				return

			if self.path.endswith('/restaurants/new'):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				output = ""
				output += "<html><body>"
				output += "<h1>Make a New Restaurant</h1>"
				output += r'''
				<form method='POST' enctype='multipart/form-data' action='/restaurants/new'>
					<input name="newRestaurantName" type="text" placeholder='New Restaurant Name'>
					<input type="submit" value="Create">
				</form>
				'''
				output += "</body></html>"
				self.wfile.write(output)
				print output
				return

		except IOError:
			self.send_error(404, 'File Not Found: %s' % self.path)


	def do_POST(self):
		try:
			if self.path.endswith("/restaurants/new"):
				ctype, pdict = cgi.parse_header(
					self.headers.getheader('content-type'))
				if ctype == 'multipart/form-data':
					fields = cgi.parse_multipart(self.rfile, pdict)
					messagecontent = fields.get('newRestaurantName')
					restaurantCURD.createNewRestaurant(messagecontent[0])

					self.send_response(301)
					self.send_header('Content-type', 'text/html')
					self.send_header('Location', '/restaurants')
					self.end_headers()

			if self.path.endswith("/edit"):
				ctype, pdict = cgi.parse_header(
					self.headers.getheader('content-type'))
				if ctype == 'multipart/form-data':
					fields = cgi.parse_multipart(self.rfile, pdict)
					messagecontent = fields.get("newRestaurantName")
					restaurantID = self.path.split("/")[2]
					restaurant = restaurantCURD.restaurantWithID(restaurantID)
					print restaurant.id
					if restaurant != []:
						restaurant.name = messagecontent[0]
						restaurantCURD.updateRestaurant(restaurant)
						self.send_response(301)
						self.send_header("Content-type", "text/html")
						self.send_header("Location", "/restaurants")
						self.end_headers()

			if self.path.endswith("/delete"):
				ctype, pdict = cgi.parse_header(
					self.headers.getheader('content-type'))
				if ctype == 'multipart/form-data':
					restaurantToDeleteID = self.path.split("/")[2]
					restaurantCURD.deleteRestaurantWithID(restaurantToDeleteID)
					self.send_response(301)
					self.send_header("content-type", "text/html")
					self.send_header("Location", "/restaurants")
					self.end_headers()
		except:
			pass 


def main():
 	try:
 	 	port = 8080
 	 	server = HTTPServer(('',port), WebserverHandler)
 	 	print "Web server running on port %s" % port
 	 	server.serve_forever()

 	except KeyboardInterrupt:
 	 	print "^C entered, stopping web server..."
 	 	server.socket.close()

if __name__ == '__main__':
	main()

			
